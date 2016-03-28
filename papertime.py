import os
import random
import time
import sys

def getRandomFile(paperPath):
  """
  Returns a random filename, chosen among the files of the given path.
  """
  files = os.listdir(paperPath)
  index = random.randrange(0, len(files))
  name = str(files[index])
  if (name != "Read" and name != ".DS_Store"):
    return name

def readingBlock(run):
    os.system("open "+'/Users/lucianne/Dropbox/PaperTime/'+filename)

def readingTimer(duration):
    mins = 0
    while mins != duration:
        print ">>>>>>>>>>>>>>>>>>>>>", mins
        # Sleep for a minute
        time.sleep(60)
        # Increment the minute total
        mins += 1
    os.system('say "Ding!"')
    print 'Time up!'

if __name__ == "__main__":
    
    filename = getRandomFile('/Users/lucianne/Dropbox/PaperTime/')
    filename = str(filename)
    if filename == "None":
        print 'No papers in directory!'
        sys.exit()

    print 'HEYYYYYYY Paper Time, Paper Time, Paper Time!'
    run = raw_input("Ready to read? > ")
    if run == "y":
        readingBlock(run)
    while run == "y":
        readingTimer(1)
        run = raw_input("Want to keep reading? (y/n) > ")
    if run == "n":
        finish = raw_input("Keep or Delete Paper? (k/d) > ")
        if finish == "k":
            os.rename('/Users/lucianne/Dropbox/PaperTime/'+filename, '/Users/lucianne/Dropbox/PaperTime/Read/'+filename)
            notefilename = filename+'_notes.txt'
            os.system("touch "+'/Users/lucianne/Dropbox/PaperTime/'+notefilename)
            os.system("open "+notefilename)
            editing = raw_input("Hit any key when finished making notes > ")
            os.rename('/Users/lucianne/Dropbox/PaperTime/'+notefilename, '/Users/lucianne/Dropbox/PaperTime/Read/'+notefilename)
        if finish == "d":
            os.system("rm "+'/Users/lucianne/Dropbox/PaperTime/'+filename)