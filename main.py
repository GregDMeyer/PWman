#!/usr/bin/env python

from Tkinter import *
from gui import App, About
import atexit

# execute everything!

root = Tk()
root.title('PWman')

def showAbout():
    top = Toplevel()
    top.title('About PWman')

    about = About( top )

    return

root.createcommand('tkAboutDialog', showAbout)

menubar = Menu(root)
root.config(menu=menubar)

app = App( root )

root.createcommand('exit', app.Quit)

#make my screen dimensions work
w = 320 #The value of the width
h = 600 #The value of the height of the window

# get screen width and height
ws = root.winfo_screenwidth() #This value is the width of the screen
hs = root.winfo_screenheight() #This is the height of the screen

# calculate position x, y
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

#This is responsible for setting the dimensions of the screen and where it is
#placed
root.geometry('+%d+%d' % (x, y))


root.mainloop()

app.Quit()
