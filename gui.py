'''
Classes for the GUI. Pretty self explanatory.
'''

from Tkinter import *
from myTkObjects import *
import copypaste
import string
import webbrowser
import aes
import tkHyperlinkManager
from os.path import isfile
import os
import cPickle
from passwordGen import make_pass
import config

from Cocoa import NSHomeDirectory
home = NSHomeDirectory()

### about window

class About:

	def __init__(self,master):

		self.master = master
		self.frame = Frame(self.master,width=350,height=500)
		self.frame.pack_propagate(False)
		self.frame.pack(fill='both',expand=True)

		self.title = myTitle(self.frame,text='ABOUT')
		self.title.pack(fill='x')

		text = '''PWman, version 2.0
'''+u'\u00A9'+'''2014 Greg Meyer

Created by Greg Meyer

Written in Python, using Tkinter

DISCLAIMER:
There is no guarantee or warranty that passwords will be safe under this program. Though AES-256 encryption is considered impossible to break without the password, a weak master password can be easy to simply guess. Please, choose a good master password!

Also, it is generally a good idea to only save passwords here that you don't know by heart, and aren't crucial to your life. Saving your social security number and banking information here probably isn't a good idea. But, saving the password that you always forget to your Twitter account is great.

SECURITY INFO:
The password data is saved under 256-bit AES encryption, which has approved by the US government for top secret documents.  50,000 iteration key stretching with a salt is implemented to prevent brute force attacks against the password.

*****

Special thanks to Sara Kahanamoku for helping me choose nice colors :)

Thanks to Jeff Zhang for using computers a lot and knowing what feels intuitive. Also for advice on the logo.

Also, thanks to the people on Stack Overflow who have an answer to any coding question in the world.

*****

PWman is open source! Check out the code here: '''

		self.text = Text(
			self.frame, 
			relief='sunken', 
			bd=2, wrap='word', 
			font=(FONT_FAMILY,12),
			highlightthickness = 0,
			)

		link = tkHyperlinkManager.HyperlinkManager(self.text)

		self.text.insert(END,text)
		self.text.insert(END,'https://github.com/GregDMeyer/PWman', link.add(self._openGithub) )

		text2 = ''' 
		
*****

LICENSE 

'''+u'\u00A9'+'''2014, Greg Meyer
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

		self.text.insert(END,text2)

		self.scrollbar = Scrollbar(self.frame)
		self.scrollbar.config(command=self.text.yview)

		self.text.config(state='disabled',yscrollcommand=self.scrollbar.set)

		self.scrollbar.pack(side=RIGHT, fill=Y)
		self.text.pack(side=LEFT,fill='both',expand=True)

		return

	def _openGithub(self,event=None):
		webbrowser.open('https://github.com/GregDMeyer/PWman')
		return



### actual app

class App:

	def __init__(self,master):

		self.master = master

		self.master.resizable(0, 0)

		self.tutorial = False

		self.warning_manager = myWarningManager( self.master )
		self.warning_manager.pack(side='bottom',fill='x')

		if not isfile(home+'/.pwman_test/passwd'):
			self.current = Welcome( self.master,self )
			self.tutorial = True
		else:
			self.current = Login( self.master,self )
			pass

		self.data = None
		self.password = None
		self.config = None

		self.clip = copypaste.Clipboard()

		self.master.bind_all('<Command-w>',self.Quit)

		return

	def change_state(self,new_state):

		# get rid of any bindings that were still around
		for char in string.ascii_letters+string.digits+string.punctuation:
			if char == '<':
				char = '<less>'
				pass
			self.current.frame.unbind_all(char)
			pass

		self.current.frame.unbind_all('<space>')

		self.current.frame.unbind_all('<BackSpace>')

		self.current.frame.unbind_all('<Return>')

		self.current.frame.pack_forget()
		self.current.frame.destroy()

		self.warning_manager.clear_all()

		self.current = new_state(self.master,self)
		return

	# set variables of data and master password
	def set_data(self,data,password,config=None):
		self.data = data
		self.data.pop(None,0) # A 'None' gets in there as a key sometimes, which is bad
		self.password = password
		self.config = config
		return

	def save_data(self):
		if not self.data is None:
			with open( home+'/.pwman_test/data', 'w' ) as f:
				f.write( aes.encrypt( cPickle.dumps([self.data, self.config]), self.password) )
		return

	def Quit(self, event=None):

		#get the old clipboard back
		self.clip.revert()

		self.master.quit()
		sys.exit()
		pass


### separate classes for each page of the GUI

# a framework class for making new pages

''' 

class framework:

	def __init__(self,master,app):

		self.app = app

		self.frame = Frame( master )
		self.frame.pack( fill='both',expand=True )

		# add buttons and menus and whatnot here

		pass

	# now add functions here which will be called by the buttons/menus above.

	# when switching to a new screen, do: self.app.change_state('new_screen_class_name',self.frame)

	# you can also quit the program with self.app.Quit()

	'''

class Welcome:

	def __init__(self,master,app):

		self.app = app
		self.master = master

		self.frame = Frame( self.master )
		self.frame.pack( fill='both',expand=True )

		self.text = myTitle( self.frame, text='WELCOME')
		self.text.pack()

		self.text = myMessage( self.frame, text='Looks like your first time!\nSet a master password for PWman:', height=2 )
		self.text.pack()

		self.pass_in = myPassEntry( self.frame, text='NEW PASSWORD',)
		self.pass_in.pack()

		self.pass_confirm = myPassEntry( self.frame, text='RETYPE PASSWORD',)
		self.pass_confirm.pack()
		self.pass_confirm.bind('<Return>',self.save)

		self.save_button = myButton( self.frame, text='SAVE', command=self.save )
		self.save_button.pack(fill='x')

		return


	def save(self, event=None):

		if self.pass_in.get() != self.pass_confirm.get():
			self.no_match()
			return

		new_pass = self.pass_in.get()

		os.makedirs(home+'/.pwman_test')

		aes.save_master_pass( new_pass )
		self.app.password = new_pass

		default_config = config.load_config_file('default.cfg')

		self.app.set_data( data={}, password=new_pass, config=default_config )

		self.app.save_data()

		self.app.change_state( mainMenu )

		return

	def no_match( self ):
		self.app.warning_manager.display_warning(name='noMatch',text='Passwords do not match!')
		return


class Login:

	def __init__(self,master,app):

		self.app = app
		self.master = master

		self.frame = Frame( self.master )
		self.frame.pack( fill='both',expand=True)

		self.text = myTitle( self.frame, text = 'PWman, v. 2.0')
		self.text.pack()

		self.passin = myPassEntry( self.frame,text='PASSWORD',)
		self.passin.bind('<Return>', self.login )
		self.passin.pack()

		#if they start typing, put focus into the password entry widget

		for char in string.ascii_letters+string.digits+string.punctuation:
			if char == '<':
				char = '<less>'
				pass
			self.frame.bind_all(char, self.on_typing)
			pass

		self.frame.bind_all('<space>', self.on_typing)

		self.loginbutton = myButton( self.frame, text = 'LOGIN', command = self.login )
		self.loginbutton.pack(fill='x')

		self.tries = 0

		if self.app.tutorial:

			self.app.warning_manager.display_warning(name='hint',text='Hint: Typing automatically jumps to the\npassword box, so you can type in your\npassword as soon as you open the app!')

		return

	def on_typing(self, event):

		for char in string.ascii_letters+string.digits+string.punctuation:
			if char == '<':
				char = '<less>'
				pass
			self.frame.unbind_all(char)
			pass

		self.frame.unbind_all('<space>')

		self.passin.focusInsert(event.char)

		return


	def login( self, event = None ):

		password = self.passin.get()

		if aes.check_pass( password ):

			data = {}
			config = {}
			if isfile(home+'/.pwman_test/data'):

				with open(home+'/.pwman_test/data') as f:
					datastring = aes.decrypt( f.read(), password )

				if datastring.strip() != '':
					data,config = cPickle.loads( datastring )

			self.app.set_data( data, password, config )
			self.app.change_state( mainMenu )

		else:
			self.login_fail()

		return

	def login_fail( self ):

		if self.tries >= 2:
			self.app.Quit()
			return

		self.app.warning_manager.display_warning(name='badPass',
			text='Incorrect password! Please try again. \n '+str(2-self.tries)+' attempt'+('s' if self.tries<1 else '')+' remaining.')

		self.passin.delete(0,END)

		self.tries += 1

		pass


class mainMenu:

	def __init__(self,master,app):

		self.app = app
		self.master = master

		self.master.bind_all('<Escape>',lambda event: self.app.change_state( mainMenu ))

		self.frame = Frame( self.master )
		self.frame.pack( fill='both',expand=True, )

		self.text = myTitle( self.frame, text = 'PWman, v. 2.0')
		self.text.pack()

		buttonList = [
		'Get',
		'New',
		'Update',
		'Remove',
		'Settings'
		]

		self.buttons = {}

		for name in buttonList:
			self.buttons[name] = myButton( self.frame, text=name.upper(), width=20, command = self.make_button_callback( eval(name) ) )
			self.buttons[name].pack(fill='both')
			pass

		# commented out because I actually like that these are enabled even if empty
		# if self.app.data == {}:
		# 	self.buttons['Update'].disable()
		# 	self.buttons['Remove'].disable()
		# 	self.buttons['Get'].disable()
		# 	pass

		self.frame.bind_all('g', self.buttons['Get'].command)
		self.frame.bind_all('n', self.buttons['New'].command)
		self.frame.bind_all('u', self.buttons['Update'].command)

		if self.app.tutorial:
			self.app.warning_manager.display_warning(name='hint',text='Hint: Typing g, n, or u will jump you to the Get,\nNew, and Update menus respectively.')

		return

	def remove_bindings(self, event=None):

		self.frame.unbind_all('g')
		self.frame.unbind_all('n')
		self.frame.unbind_all('u')
		return

	def make_button_callback(self, target):
		def make_choice(event):
			self.remove_bindings()
			self.app.change_state( target )
			pass
		return make_choice


class New:

	def __init__(self,master,app):

		self.app = app
		self.master = master

		self.frame = Frame( self.master )
		self.frame.pack( fill='both',expand=True,)

		self.text = myTitle( self.frame, text='SAVE NEW' )
		self.text.pack(fill='x')

		self.name_in = myEntry( self.frame, text='NAME' )
		self.name_in.pack(fill='x')

		self.pass_in = myShowHidePassEntry( self.frame, text='PASSWORD',)
		self.pass_in.pack()
		self.pass_in.bind('<Return>',self.save)

		self.gen_button = myButton( self.frame, text='GENERATE', color='light gray', font_size=25, command=self.gen_pass)
		self.gen_button.pack(fill='x')

		self.save_button = myButton( self.frame, text='SAVE', command=self.save )
		self.save_button.pack(fill='x')

		self.back_button = myButton( self.frame, text='MAIN MENU', command=lambda e=None: self.app.change_state( mainMenu ) )
		self.back_button.pack(fill='x')

		return


	def save(self, event=None ):

		self.app.warning_manager.clear_all()

		if self.name_in.get() in self.app.data.keys():
			self.app.warning_manager.display_warning(name='badName',text='That name is already in use!\nTry again...')

		elif self.name_in.get() == '':
			self.app.warning_manager.display_warning(name='badName',text='Please enter a name...' )

		elif self.pass_in.get() == '':
			self.app.warning_manager.display_warning(name='badPass',text='Please enter a password...' )

		else:	
			self.app.data[ self.name_in.get() ] = self.pass_in.get()
			self.app.save_data()
			self.app.change_state( mainMenu )

		return


	def gen_pass(self, event=None):

		self.pass_in.set( make_pass() )
		return


class Update:

	def __init__(self,master,app):

		self.app = app
		self.master = master

		self.frame = Frame( self.master )
		self.frame.pack( fill='both',expand=True,)

		self.title = myTitle( self.frame, text="UPDATE" )
		self.title.pack(fill='x')

		self.list = myPageList(self.frame, nameList= sorted( self.app.data.keys(), key=lambda s: s.lower() ) )
		self.list.pack(fill='x')

		self.passin = myShowHidePassEntry( self.frame, text='PASSWORD' )
		self.passin.pack(fill='x')
		self.passin.bind('<FocusIn>',self.remove_bindings)

		self.gen_button = myButton( self.frame, text='GENERATE', color='light gray', font_size=25, command=self.gen_pass)
		self.gen_button.pack(fill='x')

		self.back_button = myButton( self.frame, text='MAIN MENU', command=lambda e=None: self.app.change_state( mainMenu ) )
		self.back_button.pack(side='bottom',fill='x')

		self.save_button = myButton( self.frame, text='SAVE', command=self.save )
		self.save_button.pack(side='bottom',fill='x')

		
	def save(self, event=None):

		self.app.warning_manager.clear_all()

		if self.list.getSelection() is None:
			self.app.warning_manager.display_warning(name='noChoice',text='Choose a password to update.')
			return
			pass

		if self.passin.get() == '':
			self.app.warning_manager.display_warning(name='noPass',text='Type the new password in the PASSWORD field.')
			return

		self.app.data[ self.list.getSelection() ] = self.passin.get()
		self.app.save_data()
		self.app.change_state( mainMenu )
		pass


	def gen_pass(self, event=None):

		self.passin.set( make_pass() )
		return

	
	def remove_bindings( self, event=None ):

		for char in string.ascii_letters+string.digits+string.punctuation:
			if char == '<':
				char = '<less>'
				pass
			self.frame.unbind_all(char)
			pass

		self.frame.unbind_all('<space>')

		self.frame.unbind_all('<BackSpace>')


class Get:

	def __init__(self,master,app):

		self.app = app
		self.master = master

		self.frame = Frame( self.master )
		self.frame.pack( fill='both',expand=True )

		self.text = myTitle( self.frame, text="GET PASSWORD" )
		self.text.pack()

		self.list = myPageList(self.frame, nameList= sorted( self.app.data.keys(), key=lambda s: s.lower() ), selectionCommand=self.get_pass )
		self.list.pack()

		self.back_button = myButton( self.frame, text='MAIN MENU', command=lambda e=None: self.app.change_state( mainMenu ) )
		self.back_button.pack(fill='x')

		self.frame.bind_all('<Return>',self.on_return)

		if self.app.tutorial:
			self.app.warning_manager.display_warning(name='hint',text='Clicking on a name copies that password\nto the clipboard.\nHint: try typing some letters to filter by name,\nif you have a long list!')

	def on_return(self, event):

		if self.list.nameList:
			self.list.setSelection(0)
			pass

	def get_pass( self, event=None ):

		self.app.warning_manager.clear_all()

		if self.list.getSelection() is None:
			self.app.warning_manager.display_warning(name='noSelection',text='Select a password to get!')
			return

		self.app.clip.copy( self.app.data[ self.list.getSelection() ] )
		self.app.warning_manager.display_warning(name='copied',text='Password for:\n"'+self.list.getSelection()+'"\ncopied to clipboard.')

		pass


class Remove:

	def __init__(self,master,app):

		self.app = app
		self.master = master

		self.frame = Frame( self.master )
		self.frame.pack( fill='both',expand=True,)

		self.text = myTitle( self.frame, text="REMOVE\nPASSWORD",height=2 )
		self.text.pack()

		self.list = myPageList(self.frame, nameList= sorted( self.app.data.keys(), key=lambda s: s.lower() ),)
		self.list.pack()

		self.remove_button = myButton( self.frame, text='REMOVE', command=self.delete_pass ) #eventually decide time in config file
		self.remove_button.pack()

		self.back_button = myButton( self.frame, text='MAIN MENU', command=lambda e=None: self.app.change_state( mainMenu ) )
		self.back_button.pack()
		return


	def delete_pass( self, event ):

		self.app.warning_manager.clear_all()

		if self.list.getSelection() is None:
			self.app.warning_manager.display_warning(name='noSelection',text='Select a password to remove!')
			return

		del( self.app.data[ self.list.getSelection() ] )
		self.app.save_data()
		self.app.change_state( Remove )
		return


class Settings:

	#things to set:

	def __init__(self, master, app):

		self.app = app
		self.master = master

		self.frame = Frame( self.master )
		self.frame.pack( fill='both',expand=True,)

		self.text = myTitle( self.frame, text="SETTINGS" )
		self.text.pack()

		self.change_pass_button = myButton( self.frame, text='LOGIN PASSWORD', command=lambda e=None: self.app.change_state( ChangeMasterPass ) )
		self.change_pass_button.pack()

		self.back_button = myButton( self.frame, text='MAIN MENU', width=20, command=lambda e=None: self.app.change_state( mainMenu ) )
		self.back_button.pack(side='bottom')

		pass


class ChangeMasterPass:

	def __init__(self,master,app):

		self.app = app
		self.master = master

		self.frame = Frame( self.master )
		self.frame.pack( fill='both',expand=True, )

		self.text = myTitle( self.frame, text='MASTER PASSWORD' )
		self.text.pack()

		self.oldpass_in = myPassEntry( self.frame, text='OLD')
		self.oldpass_in.pack()

		self.pass_in = myPassEntry( self.frame, text='NEW')
		self.pass_in.pack()

		self.pass_in2 = myPassEntry( self.frame, text='CONFIRM NEW')
		self.pass_in2.pack()

		self.save_button = myButton( self.frame, text='SAVE', command=self.save )
		self.save_button.pack(fill='x')

		self.cancel_button = myButton( self.frame, text='CANCEL', command=lambda e=None: self.app.change_state( Settings ) )
		self.cancel_button.pack(side='bottom',fill='x')


	def save(self, event=None ):

		self.app.warning_manager.clear_all()

		if self.pass_in.get() != self.pass_in2.get():
			self.app.warning_manager.display_warning(name='noMatch',text='Passwords do not match!')
			return

		if not aes.check_pass( self.oldpass_in.get() ):
			self.app.warning_manager.display_warning(name='badPass',text='Old password incorrect!')
			return 

		newpass = self.pass_in.get()

		aes.save_master_pass( newpass )
		self.app.password = newpass
		self.app.save_data()

		self.app.change_state( mainMenu )

		self.app.warning_manager.display_warning(name='success',text='Successfully changed\nmaster password.')

		pass

