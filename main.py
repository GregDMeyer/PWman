#!/usr/bin/env python

'''
Launch application, put it in the correct place on the screen, etc.
'''

from Tkinter import *
from gui import App, About
import atexit

# execute everything!

root = Tk(className='pwman') # class is to keep track of the process for the launcher
root.title('PWman')

def showAbout():
    top = Toplevel()
    top.title('About PWman')

    About( top )

    return

root.createcommand('tkAboutDialog', showAbout)

menubar = Menu(root)
root.config(menu=menubar)

app = App( root )

root.createcommand('exit', app.Quit)

#make my screen dimensions work
w = 320
h = 600
# get screen width and height
ws = root.winfo_screenwidth() 
hs = root.winfo_screenheight() 

x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

root.geometry('+%d+%d' % (x, y))

root.mainloop()

app.Quit()
