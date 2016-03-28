import os
import random
import time
import sys
import schedule
from Tkinter import *
from tkMessageBox import *

def getRandomFile(paperPath):
  """
  Returns a random filename, chosen among the files of the given path.
  """
  files = os.listdir(paperPath)
  index = random.randrange(0, len(files))
  name = str(files[index])
  if (name != "Read" and name != ".DS_Store"):
    return name

def readingTimer(duration):
    mins = 0
    while mins != duration:
        print ">>>>>>>>>>>>>>>>>>>>>", mins
        # Sleep for a minute
        time.sleep(60)
        # Increment the minute total
        mins += 1
    os.system('say "Ding!"')

def heypapertime():
    
    #choose a file to read at random
    filename = getRandomFile('/Users/lucianne/Dropbox/PaperTime/')
    filename = str(filename)
    
    # exit if there are no files to read bc you have miraculously read them all
    # weirdly buggy, sometimes says None when not true?
    if filename == "None":
        print 'No papers in directory!'
        sys.exit()

    # want to launch a snippet of music here instead of the cmd-line thing

    run = askokcancel("Hey hey hey Paper Time!", "Ready to read a paper?")
    while run == True:
        # open the paper
        os.system("open "+'/Users/lucianne/Dropbox/PaperTime/'+filename)
        # run the timer - number here is in minutes, default is 25 min
        readingTimer(0)
        # when the timer ends ask if they want to keep reading
        run = askyesno("Paper Time!", "Want to keep reading?")
        
    finish = askyesno("Paper Time!", "Keep this paper?")
    if finish == True:
        os.rename('/Users/lucianne/Dropbox/PaperTime/'+filename, '/Users/lucianne/Dropbox/PaperTime/Read/'+filename)
        notefilename = filename+'_notes.txt'
        os.system("touch "+'/Users/lucianne/Dropbox/PaperTime/'+notefilename)
        os.system("open "+'/Users/lucianne/Dropbox/PaperTime/'+notefilename)
        editing = askquestion("Paper Time!", "Click when finished making notes")
        os.rename('/Users/lucianne/Dropbox/PaperTime/'+notefilename, '/Users/lucianne/Dropbox/PaperTime/Read/'+notefilename)
    else:
        os.system("rm "+'/Users/lucianne/Dropbox/PaperTime/'+filename)

# run every day at 3pm
schedule.every().day.at("15:00").do(heypapertime)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute