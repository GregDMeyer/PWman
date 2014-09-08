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

root.mainloop()

app.Quit()
