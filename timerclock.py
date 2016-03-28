# for python 3.x use 'tkinter' rather than 'Tkinter'
import Tkinter as tk
import tkFont
import datetime
import math
MINUTE = 60
HOUR = 60*MINUTE

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.customFont = tkFont.Font(family="Helvetica", size=48)
        self.done_time=datetime.datetime.now() + datetime.timedelta(seconds=1500) # half hour
        self.label = tk.Label(text="", font=self.customFont)
        self.label.pack()
        self.update_clock()
        self.root.mainloop()
    
    def update_clock(self):
        elapsed = self.done_time - datetime.datetime.now()
        h,m,s = elapsed.seconds/3600,elapsed.seconds/60,elapsed.seconds%60
        fractional_seconds = math.floor(elapsed.microseconds/1000000.0*100)
        self.label.configure(text="%02d:%02d:%02d"%(h,m,s))
        self.root.after(1000, self.update_clock)

if __name__ == '__main__':
    app=App()
