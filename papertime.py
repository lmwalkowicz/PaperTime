
#--- Default paths for papers to be read and filed away, respectively.
readDir  = '/Users/wolvebc1/Drop_box/_ReadingList/'
saveDir  = '/Users/wolvebc1/Drop_box/_ReadingList/Saved/'
nukeDir  = '/Users/wolvebc1/Drop_box/_ReadingList/Nuked/'
testMode = False # Running in "development" mode if True
runQuiet = True  # Don't "say" anything if True

import os
import sys
import time
import math
import random
import shutil
import schedule
import datetime
import tkMessageBox as tkmsg
# for python 3.x use 'tkinter' rather than 'Tkinter'
import Tkinter as tk
import tkFont

if testMode: # Let's just break things quickly and get it over with.
    delayInMinutes = 0.1
else:        # Some more realistic values
    delayInMinutes = 25

q = '"'
# We'll quote pathnames passed via os.system() for safety. Note that this breaks
# when the paper name contains a quote, which is a valid character in a filename
# on OS X. TBD - will fix eventually.

class timerClock():

    def __init__(self,delayInMinutes,filename,readDir,saveDir,nukeDir):
        if delayInMinutes==None: self.delayInMinutes = 1 
        else:                    self.delayInMinutes = delayInMinutes 
        if readDir==None:  self.readDir  = "." 
        else:              self.readDir  = readDir
        if saveDir==None:  self.saveDir  = "." 
        else:              self.saveDir  = saveDir 
        if nukeDir==None:  self.nukeDir  = "." 
        else:              self.nukeDir  = nukeDir 
        if filename==None:
            print "Something seems to have gone wrong - filename was empty!"
            sys.exit()
        else:              self.filename = filename
        self.root = tk.Tk()
        self.customFont = tkFont.Font(family="Helvetica", size=48)

        #--- Add buttons to execute actions. Experimenting with using Frames to
        #--- hold collections of child widgets to specify their location in the
        #--- parent (self.root)
        buttonRow1 = tk.Frame(self.root)
        buttonRow2 = tk.Frame(self.root)
        self.wdgt = tk.Button(buttonRow1,text="Read more" ,command=self.reset)
        self.wdgt.pack(side=tk.LEFT)
        self.wdgt = tk.Button(buttonRow1,text="Make note" ,command=self.saveIt)
        self.wdgt.pack(side=tk.RIGHT)
        self.wdgt = tk.Button(buttonRow2,text="Delete it",command=self.nukeIt,
                              bg="red")
        self.wdgt.pack(side=tk.LEFT)
        self.wdgt = tk.Button(buttonRow2,text="Finished"  ,command=self.quit)
        self.wdgt.pack(side=tk.RIGHT)
        buttonRow1.pack(side=tk.TOP,fill=tk.X)
        buttonRow2.pack(side=tk.TOP,fill=tk.X)

        #--- Create initial timer state.
        self.done_time = datetime.datetime.now() + \
                         datetime.timedelta(seconds=self.delayInMinutes*60)
        self.label = tk.Label(text="", font=self.customFont)
        self.update_time()
        self.label.pack(side=tk.BOTTOM)

        #--- Launch timer and start mainloop event handler
        self.update_clock()
        self.root.mainloop()

    def update_time(self):
        """Update the time label in the widget."""
        elapsed = self.done_time - datetime.datetime.now()
        h =  elapsed.seconds        //3600
        m = (elapsed.seconds-3600*h)//60
        s =  elapsed.seconds % 60
        if testMode:
            print self.done_time,datetime.datetime.now(),elapsed.seconds,h,m,s
        self.label.configure(text="%02d:%02d:%02d"%(h,m,s))

    def update_clock(self):
        """If we're not past expiration time, update time label & continue."""
        if self.done_time > datetime.datetime.now():
            self.update_time()
            self.root.after(1000, self.update_clock)
        else:
            if not runQuiet: os.system('say -v Bells time up')
            if testMode: print "timer expired"

    def saveIt(self):
        """Save this paper and perhaps make some notes about it."""
        source = self.readDir+self.filename
        target = self.saveDir+self.filename
        if not testMode:
            try:
                # This generally fails because we still have file open in
                # Preview.app
                os.rename(source,target)
                # Q: Might this work instead?
                # A: Seems to suffer from same problem.
               #shutil.copy2(source,target)
               #os.system("rm "+q+source+q)
            except:
                print("Unable to save (copy then delete original) paper? ")
                print("--> "+source)
                print("----> "+target)
        # Open note for comments.
        target = q+self.saveDir+self.filename+'_notes.txt'+q
        os.system("touch "+target)
        os.system("open  "+target)

    def nukeIt(self):
        """Delete this paper. It was probably bad, and it should feel bad."""
        source = self.readDir+self.filename
        target = self.nukeDir+self.filename
        if not testMode:
            try:
                os.rename(source,target)
               #shutil.copy2(source,target)
               #os.system("rm "+q+source+q)
            except:
                print("Unable to nuke paper? ")
                print("--> "+source)
                print("----> "+target)

    def reset(self):
        """Reset the timer to the original value."""
        self.done_time = datetime.datetime.now() + \
                         datetime.timedelta(seconds=self.delayInMinutes*60)
        self.update_clock()

    def quit(self):
        """Destroy the widgets and end this program."""
        self.root.destroy()
        self.root.quit()

def getRandomFile(paperPath):
  """
  Returns a random filename, chosen among the files of the given path.
  """
  files = os.listdir(paperPath)
  index = random.randrange(0, len(files))
  name = str(files[index])
  if (name != "Read" and name != ".DS_Store"):
    return name

def heypapertime():
    filename = None

    # Choose a file to read at random. Exit if there are no files to read bc you
    # have miraculously read them all. Weirdly buggy, sometimes says None when
    # not true?
    try:
        filename = getRandomFile(readDir)
        filename = str(filename)
    except:
        if not runQuiet: os.system('say -v Bells Oops')
        print "Something seems to have gone wrong! I'm so sorry."
        print "--> ",filename
        sys.exit()

    if not os.path.exists(readDir+filename):
        print "Something seems to have gone wrong! Filename was: "
        print "--> ",filename
        sys.exit()

    # Want to launch snippet of music here instead of cmd-line 'say' thing - TBD
    if not testMode:
        if not runQuiet: os.system('say -v Bells "Paper Time"')

    # Open the paper
    if not testMode: os.system("open "+q+readDir+filename+q)

    # Run timer - value here is in minutes, default set above.
    timerClock(delayInMinutes,filename,readDir,saveDir,nukeDir)

    if testMode: print "timer destroyed"
    if not runQuiet: os.system('say -v Bells all done')
    sys.exit()



if __name__ == '__main__':

    if not os.path.exists(readDir):
        print "Specified folder for papers is missing, please fix?"
        print "--> ",readDir
        sys.exit()

    if not os.path.exists(saveDir):
        print "Specified folder for read papers is missing, creating it."
        print "--> ",saveDir
        os.mkdir(saveDir, 0774)

    heypapertime()
    sys.exit()

 # Will re-enable this after development is a bit more mature.
 #  # run every day at 3pm
 #  schedule.every().day.at("15:00").do(heypapertime)

 #  while True:
 #      schedule.run_pending()
 #      time.sleep(60) # wait one minute
