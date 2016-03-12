
'''
Some custom classes I wrote to make Tk buttons, lists etc. that look pretty. Mostly changes in font, colors, style, etc. 
Notably different stuff is for example the button class below, which actually is subclassed from Tkinter's Text object.
'''

import Tkinter as tk
import tkFont
import string

FONT_FAMILY = 'Avenir Light'

class myButton( tk.Text ):

	def __init__(self,master,text='',command=None,color='green',disabled=False,font_size=30,*args,**kwargs):

		tk.Text.__init__(self,master,*args,**kwargs)

		self.tag_configure("center", justify='center')
		self.insert(tk.END,text,"center")
		self.command = command
		self.disabled = disabled
		self.state = 'inactive'

		if color == 'green':
			self.bg = 'dark green'
			self.fg = 'papaya whip'
			self.activeColor = 'forest green'
			self.disabledFg = 'papaya whip'
			self.disabledBg = 'dark sea green'
			pass
		elif color == 'gray':
			self.bg = 'gray30'
			self.fg = 'papaya whip'
			self.activeColor = 'gray45'
			self.highlight = 'light sky blue'
			self.disabledFg = 'slate gray'
			self.disabledBg = 'gray20'
			pass
		elif color == 'light gray':
			self.bg = 'gray70'
			self.fg = 'dark slate gray'
			self.activeColor = 'gray85'
			self.disabledFg = 'slate gray'
			self.disabledBg = 'gray78'
		elif color == 'dark blue':
			self.bg = 'navy'
			self.fg = 'light sky blue'
			self.activeColor = 'RoyalBlue4'
		else:
			raise Exception(color+' is not a valid color.')
			pass

		self.config(
			font=(FONT_FAMILY,font_size),
			state='disabled',
			cursor='arrow',
			height=1,
			relief='flat',
			bd=1,
			width=20,
			pady=5,
			highlightthickness=2,
			highlightcolor=self.bg,
			highlightbackground=self.bg,
			)
		if self.disabled:
			self.config(
				bg=self.disabledBg,
				fg=self.disabledFg,
				)
		else:
			self.config(
				bg=self.bg,
				fg=self.fg,
				)
		self.config(*args,**kwargs)

		if not self.disabled:
			self.bind('<Enter>',self._MouseIn)
			self.bind('<Leave>',self._MouseOut)
			self.bind('<Button-1>',self._MouseDown)
			self.bind('<ButtonRelease-1>',self._MouseUp)
			pass

		self.mouse = {
			'in':False,
			'down':False
		}

		self.active = False

	def _MouseIn(self,event):

		#print 'Mouse in.'
		self.mouse['in'] = True
		self.config(bg=self.activeColor,)
		if not self.active:
			self.config(highlightcolor=self.activeColor,highlightbackground=self.activeColor)
		if self.state == 'clicking':
			self.config(relief='sunken')
		pass

	def _MouseOut(self,event):

		#print 'Mouse out.'
		self.mouse['in'] = False
		self.config(relief='flat')
		self.config(bg=self.bg,)
		if not self.active:
			self.config(highlightcolor=self.bg,highlightbackground=self.bg)
		pass

	def _MouseDown(self,event):

		#print 'Mouse down.'
		self.mouse['down'] = True
		if self.mouse['in']:
			self.config( relief='sunken' )
			self.state = 'clicking'
			pass
		pass

	def _MouseUp(self,event):

		#print 'Mouse up.'
		self.mouse['down'] = False
		self.config(relief='flat')
		if self.mouse['in']:
			self.state = 'active'
			pass
		else:
			self.state = 'inactive'
			pass
		if self.mouse['in'] and self.command:
			self.command( event )
			pass
		pass

	def makeActive(self):

		self.active = True

		self.config(highlightcolor=self.highlight)
		self.config(highlightbackground=self.highlight)
		pass

	def makeInactive(self):

		self.active = False

		self.config(highlightcolor=self.bg)
		self.config(highlightbackground=self.bg)

		pass

	def disable(self):

		self.config(
				bg=self.disabledBg,
				fg=self.disabledFg,
				)

		self.unbind('<Enter>',)
		self.unbind('<Leave>',)
		self.unbind('<Button-1>',)
		self.unbind('<ButtonRelease-1>',)

	def enable(self):

		self.config(
				bg=self.bg,
				fg=self.fg,
				)

		self.bind('<Enter>',self._MouseIn)
		self.bind('<Leave>',self._MouseOut)
		self.bind('<Button-1>',self._MouseDown)
		self.bind('<ButtonRelease-1>',self._MouseUp)

	def changeText(self, newtext):

		self.config(state='normal')
		self.delete(1.0,tk.END)
		self.insert(tk.END,newtext,"center")
		self.config(state='disabled')



class myEntry( tk.Entry, object ):

	def __init__(self,master,text='',isPassword=False,*args,**kwargs):

		tk.Entry.__init__(self,master,*args,**kwargs)

		self.bg='light sky blue'

		self.config(
			font=(FONT_FAMILY,30),
			width=20,
			relief='flat',
			bg='light sky blue',
			highlightthickness=2,
			highlightcolor=self.bg,
			highlightbackground=self.bg,
			fg='dodger blue',
			)
		self.config(
			*args,
			**kwargs
			)

		self.text = text
		self.empty = True
		self.insert(tk.END,self.text)

		self.bind('<FocusIn>', self.FocusIn )
		self.bind('<FocusOut>', self.FocusOut )

	def FocusIn( self, event ):

		if self.empty:
			self.delete(0,tk.END)
			self.config(fg='navy')
			self.empty = False

		pass

	def FocusOut( self, event ):

		if not self.get():

			self.empty = True
			self.config(fg='dodger blue')
			self.insert(tk.END,self.text)

		else:

			self.empty = False
			pass

	# FUNCTIONS FOR EXTERNAL USE

	def pack(self,*args,**kwargs):

		if not 'ipady' in kwargs.keys():
			kwargs['ipady'] = 5
			pass

		super(myEntry,self).pack(*args,**kwargs)
		pass

	def get(self,*args,**kwargs):

		if self.empty:
			return ''
		else:
			return super(myEntry,self).get(*args,**kwargs)
			pass



class myPassEntry( tk.Entry, object ):

	def __init__(self,master,text='',showable=False,*args,**kwargs):

		tk.Entry.__init__(self,master,*args,**kwargs)

		self.bg='light sky blue'

		self.config(
			font=(FONT_FAMILY,30),
			width=20,
			relief='flat',
			bg='light sky blue',
			highlightthickness=2,
			highlightcolor=self.bg,
			highlightbackground=self.bg,
			fg='dodger blue',
			)
		self.config(
			*args,
			**kwargs
			)

		self.text = text
		self.empty = True
		self.insert(tk.END,self.text)

		self.showable = showable

		self.bind('<FocusIn>', self.FocusIn )
		self.bind('<FocusOut>', self.FocusOut )

	def FocusIn( self, event=None ):

		if self.empty:
			self.delete(0,tk.END)
			self.config(fg='navy')
			self.config(show='*')
			self.empty = False


		pass

	def FocusOut( self, event ):

		if not self.get():

			self.empty = True
			self.config(show='',fg='dodger blue')
			self.insert(tk.END,self.text)

		else:

			self.empty = False
			pass

	# FUNCTIONS FOR EXTERNAL USE

	def pack(self,*args,**kwargs):

		if not 'ipady' in kwargs.keys():
			kwargs['ipady'] = 5
			pass

		super(myPassEntry,self).pack(*args,**kwargs)
		pass

	def get(self,*args,**kwargs):

		if self.empty:
			return ''
		else:
			return super(myPassEntry,self).get(*args,**kwargs)
			pass


	def focusInsert(self, char):

		self.unbind('<FocusIn>')

		self.focus_set()

		self.delete(0,tk.END)
		self.config(fg='navy')
		self.config(show='*')
		self.empty = False

		self.insert(tk.END, char)

		self.bind('<FocusIn>', self.FocusIn )

		return



class myShowHidePassEntry( tk.Frame, object ):

	def __init__(self,master,text='',showable=False,*args,**kwargs):

		tk.Frame.__init__(self,master,*args,**kwargs)

		self.entry = tk.Entry(self)

		self.bg='light sky blue'

		self.entry.config(
			font=(FONT_FAMILY,30),
			width=18,
			relief='flat',
			bg=self.bg,
			highlightthickness=2,
			highlightcolor=self.bg,
			highlightbackground=self.bg,
			fg='dodger blue',
			)
		self.entry.pack(ipady=5,side='left')

		self.togglebutton = myButton(self,width='2',text='a',command=self.ToggleShow,color='dark blue')
		self.togglebutton.pack(side='right',fill='y')

		self.text = text
		self.empty = True
		self.entry.insert(tk.END,self.text)

		self.show = False

		self.showable = showable

		self.entry.bind('<FocusIn>', self.FocusIn )
		self.entry.bind('<FocusOut>', self.FocusOut )

		self.focusInCommand = None
		self.focusOutCommand = None

	def FocusIn( self, event ):

		if self.focusInCommand:
			self.focusInCommand()
			pass

		if self.focusOutCommand:
			self.focusOutCommand()
			pass

		if self.empty:
			self.entry.delete(0,tk.END)
			self.entry.config(fg='navy')
			if not self.show:
				self.entry.config(show='*')
				pass
			self.empty = False


		pass

	def FocusOut( self, event ):

		if not self.get():

			self.empty = True
			self.entry.config(show='',fg='dodger blue')
			self.entry.insert(tk.END,self.text)

		else:

			self.empty = False
			pass

	def ToggleShow(self,event):

		if self.togglebutton.get(1.0,tk.END).strip() == 'a':
			self.entry.config(show='')
			self.show = True
			self.togglebutton.changeText('*')
			pass
		else:
			if not self.empty:
				self.entry.config(show='*')
				pass
			self.show = False
			self.togglebutton.changeText('a')
			pass


	def get(self,*args,**kwargs):

		if self.empty:
			return ''
		else:
			return self.entry.get(*args,**kwargs)
			pass


	def set(self, val):

		self.entry.delete(0,tk.END)
		self.entry.insert(tk.END,val)
		self.entry.config(fg='navy')

		if not self.show:
			self.entry.config(show='*')

		self.empty = False
		return


	def bind(self,*args,**kwargs):

		if '<FocusIn>' in args or '<FocusOut>' in args:

			self._myBind(*args,**kwargs)
			return

		self.entry.bind(*args,**kwargs)
		pass

	def _myBind(self, *args, **kwargs):

		if args[0] == '<FocusIn>':
			self.focusInCommand = args[1]
			pass
		elif args[0] == '<FocusOut>':
			self.focusOutCommand = args[1]
			pass
		else:
			raise Exception('Something\'s broken in _myBind in myShowHidePassEntry.')


class myTitle( tk.Text ):

	def __init__(self,master,text='',**options):

		tk.Text.__init__(self,master,**options)

		self.tag_configure("center", justify='center')
		self.insert(tk.END,text,"center")

		self.bg='old lace'

		self.config(
			font=(FONT_FAMILY,30),
			state='disabled',
			cursor='arrow',
			height=1,
			relief='flat',
			bd=1,
			width=20,
			pady=10,
			bg='old lace',
			highlightthickness=2,
			highlightcolor=self.bg,
			highlightbackground=self.bg,
			fg='OrangeRed4',
			)


class myMessage( tk.Text, object ):

	def __init__(self,master,text='',*args,**kwargs):

		tk.Text.__init__(self,master,*args,**kwargs)

		self.tag_configure("center", justify='center')
		self.insert(tk.END,text,"center")

		self.bg='old lace'

		self.config(
			font=(FONT_FAMILY,15),
			state='disabled',
			cursor='arrow',
			relief='flat',
			bd=1,
			height=1,
			width=30,
			bg='old lace',
			highlightthickness=2,
			highlightcolor=self.bg,
			highlightbackground=self.bg,
			fg='OrangeRed4',
			)
		self.config(*args,**kwargs)

	def pack( self,*args,**kwargs ):

		kwargs[ 'fill' ] = 'x'

		super(myMessage,self).pack(*args,**kwargs)


class ScrollableFrame( tk.Frame, object):
	
	def __init__(self, master):

		self.master = master

		tk.Frame.__init__(self, self.master)

		self.canvas = tk.Canvas( self.master , borderwidth=0)

		self.frame = tk.Frame( self.canvas )

		self.canvas.pack(side="left", fill="both", expand=True)
		self.canvas.create_window((0,0), window=self.frame, anchor="nw", 
								  tags="self.frame")
		self.canvas.config(yscrollincrement=0.005)

		self.canvas.bind_all("<MouseWheel>", self.OnMouseWheel )

	def OnMouseWheel(self, event):

		self.canvas.yview_scroll(-1*event.delta, "units")
		pass



class myDoubleButton( tk.Frame, object):

	def __init__(self, master, leftText='', rightText='', leftCommand=None, rightCommand=None, leftDisabled=True, rightDisabled=False, width=20,):

		self.master = master

		color='light gray'

		tk.Frame.__init__(self, self.master, borderwidth=0) # this is only OK for light gray... yeah

		self.button0 = myButton(self, width=width/2, color=color, text=leftText, command=leftCommand, highlightthickness=0, bd=1, disabled=leftDisabled)
		self.button0.pack(side='left',fill='x',expand=True)

		self.button1 = myButton(self, width=width/2, color=color, text=rightText, command=rightCommand, highlightthickness=0, bd=1, disabled=rightDisabled)
		self.button1.pack(side='left',fill='x',expand=True)

		pass

	def SetLeftDisabled(self, val = True):

		if val:
			self.button0.disable()
			#print 'disable left'
			pass
		else:
			self.button0.enable()
			#print 'enable left'
			pass

		return

	def SetRightDisabled(self, val = True):

		if val:
			self.button1.disable()
			#print 'disable right'
			pass
		else:
			self.button1.enable()
			#print 'enable right'
			pass



class myPageList( tk.Frame, object):

	def __init__(self, master, nameList, switchCommand=None, selectionCommand=None, width=20):

		self.master = master
		self.switchCommand = switchCommand
		self.selectionCommand = selectionCommand

		tk.Frame.__init__(self, self.master)

		self.showedStart = 0

		self.fullNameList = nameList

		self.nameList = nameList

		self.showedButtons = []

		self.selection = None

		self.filter = ''

		# bind all keys to filter

		for char in string.ascii_letters+string.digits+string.punctuation:
			if char == '<':
				char = '<less>'
				pass
			self.bind_all(char, self.keyPressed)
			pass

		self.bind_all('<space>', self.keyPressed)

		self.bind_all('<BackSpace>', self.BSPressed)

		# display buttons. We will only change names and colors after this, not repack them.

		for i in xrange(5):
			self.showedButtons.append( myButton( self , text='', command=self.choiceMade, color='gray' ) )
			self.showedButtons[-1].pack(fill='x')

			pass

		if len( self.fullNameList ) > 5:
			self.moreButton = myDoubleButton(
				self, 
				leftText='< BACK', 
				rightText='MORE >', 
				leftCommand=self.backChoices,
				rightCommand=self.nextChoices,
				leftDisabled = True
				#color='light gray',
				)
			self.moreButton.pack(side='bottom',fill='x')

		self.displayList()

		self.filter = ''

	def BSPressed(self,event):

		self.selection = None

		for button in self.showedButtons:
			button.makeInactive()
			pass

		self.filter = self.filter[:-1]

		self.nameList = [x for x in self.fullNameList if self.filter.lower() in x.lower()]

		self.showedStart = 0

		self.displayList()


	def keyPressed(self,event):

		self.selection = None

		for button in self.showedButtons:
			button.makeInactive()
			pass

		# don't keep adding letters if there is nothing left of the list!
		if not self.nameList:
			return

		self.filter += event.char

		self.nameList = [x for x in self.fullNameList if self.filter.lower() in x.lower()]

		self.showedStart = 0

		self.displayList()


	def displayList(self):

		try:
			self.passIn.pack_forget()
			pass
		except AttributeError:
			pass

		for button in self.showedButtons:
			button.makeInactive()
			pass

		for i in xrange( min(5,len(self.nameList) - self.showedStart)):

			self.showedButtons[i].enable()
			self.showedButtons[i].changeText(self.nameList[self.showedStart + i])
			pass

		for i in xrange( min(5,len(self.nameList) - self.showedStart), 5 ):

			self.showedButtons[i].disable()
			self.showedButtons[i].changeText('')
			pass

		if len(self.fullNameList) > 5:

			if self.showedStart == 0:
				self.moreButton.SetLeftDisabled(True)
				pass
			else:
				self.moreButton.SetLeftDisabled(False)
				pass
			if self.showedStart+5 >= len( self.nameList ):
				self.moreButton.SetRightDisabled(True)
				pass
			else:
				self.moreButton.SetRightDisabled(False)
			pass

		pass

	def nextChoices(self, event):

		if self.showedStart + 5 >= len(self.nameList):
			return

		self.showedStart += 5

		if self.switchCommand:
			self.switchCommand()
			pass

		self.displayList()

		self.selection = None

		pass

	def backChoices(self, event):

		if self.showedStart - 5 < 0:
			if self.showedStart:
				self.showedStart = 5
				pass
			else:
				return

		self.showedStart -= 5

		if self.switchCommand:
			self.switchCommand()
			pass

		self.displayList()

		self.selection = None

		pass

	def choiceMade( self, event):

		self.selection = event.widget.get(1.0,tk.END).strip()

		for button in self.showedButtons:
			button.makeInactive()
			pass
			
		event.widget.makeActive()

		if self.selectionCommand:
			self.selectionCommand()
			pass

	def setSelection( self, index ):

		theButton = self.showedButtons[ index ]

		self.selection = theButton.get(1.0,tk.END).strip()

		for button in self.showedButtons:
			button.makeInactive()
			pass
			
		theButton.makeActive()

		if self.selectionCommand:
			self.selectionCommand()
			pass

	def getSelection( self ):

		return self.selection

	def getPassword( self ):

		if not self.selection:
			return None

		return self.passIn.get()

	def destroy( self ):

		for char in string.ascii_letters+string.digits+string.punctuation:
			if char == '<':
				char = '<less>'
				pass
			self.unbind_all(char)
			pass

		self.unbind_all('<space>')

		self.unbind_all('<BackSpace>')

		super(myPageList,self).destroy()

		return



class myWarningManager( tk.Frame, object ):

	def __init__(self, master):

		self.master = master

		tk.Frame.__init__(self,self.master,height=0)

		self.warnings = {}

	# show a new warning
	def display_warning(self, name, text):

		# if this one already exists, it is cleared and replaced.
		if name in self.warnings.keys():
			self.warnings[ name ].pack_forget()
			self.warnings[ name ].destroy()
			pass

		numLines = text.count('\n') + 1

		self.warnings[ name ] = myMessage( self, text = text, height = numLines)
		self.warnings[ name ].pack(fill='x')

		if not self.winfo_ismapped():
			self._pack()
			pass

	# clear warning with name 'name'
	def clear(self, name):

		if not name in self.warnings.keys():

			raise Exception('There is no warning with name \''+name+'\'.')

		self.warnings[ name ].pack_forget()
		self.warnings[ name ].destroy()

		self.warnings.pop( name )

		if not self.warnings:
			self.pack_forget()
			pass


	# try to clear warning with name 'name', if it doesn't exist, that's fine.
	def try_clear(self, name):

		if not name in self.warnings.keys():
			return

		self.warnings[ name ].pack_forget()
		self.warnings[ name ].destroy()

		self.warnings.pop( name )

		if not self.warnings:
			self.pack_forget()
			pass


	# clear all warnings present.
	def clear_all(self):

		for child in self.winfo_children():
			child.pack_forget()
			child.destroy()

		self.warnings = {}

		self.pack_forget()

	# this one packs individual warnings
	def _pack(self):

		if self.packing:
			super(myWarningManager,self).pack(*self.pack_args,**self.pack_kwargs)
			pass

		return

	# this is to "pack" the larger warning manager class
	def pack(self,*args,**kwargs):

		self.pack_args = args
		self.pack_kwargs = kwargs

		self.packing = True
		return

