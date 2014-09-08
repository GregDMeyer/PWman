from Tkinter import *
import tkMessageBox
from myTkObjects import *
import tkFont
import machinery
import copypaste
import string
import time

### about window

class About:

	def __init__(self,master):

		self.master = master
		self.frame = Frame(self.master,width=300,height=500)
		self.frame.pack_propagate(False)
		self.frame.pack(fill='both',expand=True)

		self.title = myTitle(self.frame,text='ABOUT')
		self.title.pack(fill='x')

		text = '''PWman, version 2.0

Created by Greg Meyer

Written in Python, using Tkinter

DISCLAIMER:
There is no guarantee that passwords will be safe under this program. Though AES-256 encryption is considered impossible to break without the password, a weak master password can be easy to simply guess. Please, choose a good master password!

Also, it is generally a good idea to only save passwords here that you don't know by heart, and aren't crucial to your life. Saving your social security number and banking information here probably isn't a good idea. But, saving the password that you always forget to your Twitter account is probably fine.

SECURITY INFO:
The password data is saved under 256-bit AES encryption, which has approved by the US government for top secret documents.  50,000 iteration key stretching with a salt is implemented to prevent brute force attacks against the password.

*****

Special thanks to Sara Kahanamoku for helping me choose nice colors :)

Also, thanks to the people on Stack Overflow who have an answer to any coding question in the world.'''

		self.text = Text(
			self.frame, 
			relief='sunken', 
			bd=2, wrap='word', 
			font=(FONT_FAMILY,12),
			highlightthickness = 0,
			)

		self.text.insert(END,text)
		self.text.config(state='disabled')

		self.text.pack(fill='both',expand=True)

		return



### actual app

class App:

	def __init__(self,master):

		self.master = master

		self.master.resizable(0, 0)

		self.tutorial = False

		if machinery.FirstTime():
			self.current = Welcome( self.master,self )
			self.tutorial = True
		else:
			self.current = login( self.master,self )
			pass

		self.data = None
		self.password = None
		self.oldClip = copypaste.paste()

		self.warningManager = myWarningManager( self.master )
		self.warningManager.pack(side='bottom',fill='x')

		self.master.bind_all('<Command-w>',self.Quit)

		return

	def ChangeState(self,newstate):

		self.current.frame.pack_forget()
		self.current.frame.destroy()

		self.warningManager.clearAll()

		self.current = newstate(self.master,self)
		pass

	# set variables of data and master password
	def SetData(self,theData,thePassword):

		self.data = theData
		self.data.pop(None,0)
		self.password = thePassword
		pass

	def SaveData(self):
		if not self.data is None:
			machinery.WriteFile( self.data, self.password )
			pass
		pass

	def Quit(self, event=None):

		#get the old clipboard back
		copypaste.copy( self.oldClip )

		self.master.quit()

		sys.exit()

		pass

### separate classes for each page

# an empty class for making new pages

''' 

class framework:

	def __init__(self,master,app):

		self.app = app

		self.frame = Frame( master )
		self.frame.pack( fill='both',expand=True )

		# add buttons and menus and whatnot here

		pass

	# now add functions here which will be called by the buttons/menus above.

	# when switching to a new screen, do: self.app.ChangeState('new_screen_class_name',self.frame)

	# you can also quit the program with self.app.Quit()

	'''

class Welcome:

	def __init__(self,master,app):

		self.app = app
		self.master = master

		self.frame = Frame( self.master )
		self.frame.pack( fill='both',expand=True,)

		self.text = myTitle( self.frame, text='WELCOME')
		self.text.pack()

		self.text = myMessage( self.frame, text='Looks like your first time!\nSet a master password for PWman:', height=2 )
		self.text.pack()

		self.pass_in = myPassEntry( self.frame, text='NEW PASSWORD',)
		self.pass_in.pack()

		self.pass_in2 = myPassEntry( self.frame, text='RETYPE PASSWORD',)
		self.pass_in2.pack()
		self.pass_in2.bind('<Return>',self.Save)

		self.save_button = myButton( self.frame, text='SAVE', command=self.Save )
		self.save_button.pack()


	def Save(self, event=None):

		if self.pass_in.get() != self.pass_in2.get():

			self.NoMatch()
			return

		newpass = self.pass_in.get()

		machinery.SaveMasterPass( newpass )
		self.app.password = newpass
		self.app.SaveData()

		self.app.SetData( {}, newpass )

		self.app.ChangeState( mainMenu )

		pass

	def NoMatch( self ):

		self.app.warningManager.displayWarning(name='noMatch',text='Passwords do not match!')

		pass




class login:

	def __init__(self,master,app):

		self.app = app
		self.master = master

		self.frame = Frame( self.master )
		self.frame.pack( fill='both',expand=True)

		self.text = myTitle( self.frame, text = 'PWman, v. 2.0')
		self.text.pack()

		self.passin = myPassEntry( self.frame,text='PASSWORD',)
		self.passin.bind('<Return>', self.run )
		self.passin.pack()

		#if they start typing, put focus into the password entry widget

		for char in string.ascii_letters+string.digits+string.punctuation:
			if char == '<':
				char = '<less>'
				pass
			self.frame.bind_all(char, self.onTyping)
			pass

		self.frame.bind_all('<space>', self.onTyping)

		self.loginbutton = myButton( self.frame, text = 'LOGIN', command = self.run )
		self.loginbutton.pack(fill='x')

		self.nTries = 0

		if self.app.tutorial:

			tkMessageBox.showinfo('Tutorial','Typing automatically jumps to the password box, so you can type in your password as soon as you open the app!')

		return

	def onTyping(self, event):

		for char in string.ascii_letters+string.digits+string.punctuation:
			if char == '<':
				char = '<less>'
				pass
			self.frame.unbind_all(char)
			pass

		self.frame.unbind_all('<space>')


		# should write member function of passin to do this. otherwise it isn't working. for some reason it waits until the end of this function to change the focus, so it will delete the newly inserted character as soon as it does. 
		self.passin.focusInsert(event.char)

		return


	def run( self, event = None ):

		string = self.passin.get()

		if machinery.CheckPassword( string ):
			self.app.SetData( machinery.GetData( string ), string )
			self.app.ChangeState( mainMenu )
			pass
		else:
			self.LoginFail()
			pass

		return

	def LoginFail( self ):

		if self.nTries >= 2:
			self.app.Quit()
			return

		self.app.warningManager.displayWarning(name='badPass',text='Incorrect password! Try again...')

		self.passin.delete(0,END)

		self.nTries += 1

		pass


class mainMenu:

	def __init__(self,master,app):

		self.app = app
		self.master = master

		self.frame = Frame( self.master, bg='chartreuse4' )
		self.frame.pack( fill='both',expand=True, )

		self.text = myTitle( self.frame, text = 'PWman, v. 2.0')
		self.text.pack()

		self.buttonSetup = {
			'New' : self.FNew,
			'Update' : self.FUpdate,
			'Get' : self.FGet,
			'Remove' : self.FRemove,
			'Settings' : self.FSettings,
		}

		buttonList = [
		'Get',
		'New',
		'Update',
		'Remove',
		'Settings'
		]

		self.buttons = {}

		for name in buttonList:
			self.buttons[name] = myButton( self.frame, text=name.upper(), width=20, command = self.buttonSetup[name],)
			self.buttons[name].pack(fill='both')
			pass

		if self.app.data == {}:
			self.buttons['Update'].config(state='disabled')
			self.buttons['Remove'].config(state='disabled')
			self.buttons['Get'].config(state='disabled')
			pass

		self.frame.bind_all('g',self.FGet)
		self.frame.bind_all('n',self.FNew)
		self.frame.bind_all('u',self.FUpdate)

		if self.app.tutorial:
			tkMessageBox.showinfo('Tutorial','Typing g, n, or u will jump you to the Get, New, and Update menus respectively.')

		return

	def remove_bindings(self, event=None):

		self.frame.unbind_all('g')
		self.frame.unbind_all('n')
		self.frame.unbind_all('u')
		pass

	def FNew(self, event):
		self.remove_bindings()
		self.app.ChangeState( New )
		pass

	def FUpdate(self, event):
		self.remove_bindings()
		self.app.ChangeState( Update )
		pass

	def FGet(self, event):
		self.remove_bindings()
		self.app.ChangeState( Get )
		pass

	def FRemove(self, event):
		self.remove_bindings()
		self.app.ChangeState( Remove )
		pass

	def FSettings(self, event):
		self.remove_bindings()
		self.app.ChangeState( Settings )
		pass




class New:

	def __init__(self,master,app):

		self.app = app
		self.master = master

		self.frame = Frame( self.master )
		self.frame.pack( fill='both',expand=True,)

		self.text = myTitle( self.frame, text='SAVE NEW' )
		self.text.pack()

		self.serv_name_in = myEntry( self.frame, text='NAME' )
		self.serv_name_in.pack(fill='x')

		self.serv_pass_in = myShowHidePassEntry( self.frame, text='PASSWORD',)
		self.serv_pass_in.pack()

		# self.showpass = IntVar()

		# self.show_pass_button = Checkbutton( self.frame, text='Show password', var=self.showpass, command=self.toggleShow )
		# self.show_pass_button.pack(pady=5)

		self.save_button = myButton( self.frame, text='SAVE', command=self.Save )
		self.save_button.pack(fill='x')

		self.backMainMenu = myButton( self.frame, text='MAIN MENU', command=self.goMainMenu )
		self.backMainMenu.pack(fill='x')

		if self.app.tutorial:
			tkMessageBox.showinfo('Tutorial','Pressing the \'a\' button in the right part of the password field shows the password; pressing it a second time hides it again. If you\'re alone, this can be useful to make sure you got the password right!')

	def toggleShow(self):

		if self.showpass.get():
			self.serv_pass_in.config(show='')
			pass
		else:
			self.serv_pass_in.config(show='*')
			pass

	def Save(self, event=None ):

		self.app.warningManager.clearAll()

		if self.serv_name_in.get() in self.app.data.keys():
			self.app.warningManager.displayWarning(name='badName',text='That name is already in use!\nTry again...')

		elif self.serv_name_in.get() == '':
			self.app.warningManager.displayWarning(name='badName',text='Please enter a name...' )

		elif self.serv_pass_in.get() == '':
			self.app.warningManager.displayWarning(name='badPass',text='Please enter a password...' )

		else:	
			self.app.data[ self.serv_name_in.get() ] = self.serv_pass_in.get()
			self.app.SaveData()
			self.app.ChangeState( mainMenu )
			pass

		pass

	def goMainMenu( self, event=None ):

		self.app.ChangeState( mainMenu )
		pass


class Update:

	def __init__(self,master,app):

		self.app = app
		self.master = master

		self.frame = Frame( self.master )
		self.frame.pack( fill='both',expand=True,)

		self.title = myTitle( self.frame, text="UPDATE" )
		self.title.pack(fill='x')

		# self.showpass = IntVar()

		# self.show_pass_button = Checkbutton( self.frame, text='Show password', var=self.showpass, command=self.toggleShow )
		# self.show_pass_button.pack(pady=5)

		self.list = myPageList(self.frame, nameList= sorted( self.app.data.keys(), key=lambda s: s.lower() ) )
		self.list.pack(fill='x')

		self.passin = myShowHidePassEntry( self.frame, text='PASSWORD' )
		self.passin.pack(fill='x')

		self.passin.bind('<FocusIn>',self.removeBindings)

		self.backMainMenu = myButton( self.frame, text='MAIN MENU', command=self.goMainMenu )
		self.backMainMenu.pack(side='bottom',fill='x')

		self.save_button = myButton( self.frame, text='SAVE', command=self.Save )
		self.save_button.pack(side='bottom',fill='x')

		if self.app.tutorial:
			tkMessageBox.showinfo('Tutorial','Like in the \'Get\' menu, typing some letters will filter the list shown. When you\'ve found the password you want to update, click on it, and type the new password into the \'PASSWORD\' box.')

	def toggleShow(self):

		if self.showpass.get():
			self.serv_pass_in.config(show='')
			pass
		else:
			self.serv_pass_in.config(show='*')
			pass
		
	def Save(self, event=None):

		self.app.warningManager.clearAll()

		if self.list.getSelection() is None:
			self.app.warningManager.displayWarning(name='noChoice',text='Choose a password to update.')
			return
			pass

		if self.passin.get() == '':
			self.app.warningManager.displayWarning(name='noPass',text='Type the new password in the PASSWORD field.')
			return

		self.app.data[ self.list.getSelection() ] = self.passin.get()
		self.app.SaveData()
		self.app.ChangeState( mainMenu )
		pass

	def removeBindings( self, event=None ):

		for char in string.ascii_letters+string.digits+string.punctuation:
			if char == '<':
				char = '<less>'
				pass
			self.frame.unbind_all(char)
			pass

		self.frame.unbind_all('<space>')

		self.frame.unbind_all('<BackSpace>')


	def goMainMenu( self, event=None ):

		self.app.ChangeState( mainMenu )
		pass

class Get:

	def __init__(self,master,app):

		self.app = app
		self.master = master

		self.frame = Frame( self.master )
		self.frame.pack( fill='both',expand=True )

		self.text = myTitle( self.frame, text="GET PASSWORD" )
		self.text.pack()

		self.list = myPageList(self.frame, nameList= sorted( self.app.data.keys(), key=lambda s: s.lower() ), selectionCommand=self.GetPass )
		self.list.pack()

		self.backMainMenu = myButton( self.frame, text='MAIN MENU', command=self.goMainMenu )
		self.backMainMenu.pack(fill='x')

		self.frame.bind_all('<Return>',self.onReturn)

		if self.app.tutorial:
			tkMessageBox.showinfo('Tutorial','Select a password to get by clicking on it. The password will automatically be copied to the clipboard, so that it never has to be shown on the screen. The blue box around the name signifies that it is on the clipboard. Hint: try typing some letters to filter by name, if you have a long list!')

	def onReturn(self, event):

		if self.list.nameList:
			self.list.setSelection(0)
			pass

	def GetPass( self, event=None ):

		self.app.warningManager.clearAll()

		if self.list.getSelection() is None:
			self.app.warningManager.displayWarning(name='noSelection',text='Select a password to get!')
			return

		machinery.CopyPass( self.app.data[ self.list.getSelection() ], 20 )

		#self.app.ChangeState( mainMenu )

		pass

	def goMainMenu( self, event=None ):

		self.app.ChangeState( mainMenu )
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

		self.save_button = myButton( self.frame, text='REMOVE', command=self.DeletePass ) #eventually decide time in config file
		self.save_button.pack()

		self.backMainMenu = myButton( self.frame, text='MAIN MENU', command=self.goMainMenu )
		self.backMainMenu.pack()

	def DeletePass( self, event ):

		self.app.warningManager.clearAll()

		if self.list.getSelection() is None:
			self.app.warningManager.displayWarning(name='noSelection',text='Select a password to remove!')
			return

		del( self.app.data[ self.list.getSelection() ] )
		self.app.SaveData()
		self.app.ChangeState( mainMenu )
		pass

	def goMainMenu( self, event=None ):

		self.app.ChangeState( mainMenu )
		pass

class Settings:

	#things to set:

	def __init__(self, master, app):

		self.app = app
		self.master = master

		self.frame = Frame( self.master )
		self.frame.pack( fill='both',expand=True,)

		self.text = myTitle( self.frame, text="SETTINGS" )
		self.text.pack()

		self.changeMasterPass = myButton( self.frame, text='LOGIN PASSWORD', command = self.changeMasterPass, )
		self.changeMasterPass.pack()

		self.backMainMenu = myButton( self.frame, text='MAIN MENU', width=20, command=self.goMainMenu )
		self.backMainMenu.pack(side='bottom')

		pass

	def changeMasterPass( self, event=None ):

		self.app.ChangeState( ChangeMasterPass )
		pass

	def goMainMenu( self, event=None ):

		self.app.ChangeState( mainMenu )
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

		self.save_button = myButton( self.frame, text='SAVE', command=self.Save )
		self.save_button.pack()

		self.cancel_button = myButton( self.frame, text='CANCEL', command=self.Cancel )
		self.cancel_button.pack(side='bottom',)


	def Save(self, event=None ):

		self.app.warningManager.clearAll()

		if self.pass_in.get() != self.pass_in2.get():

			self.app.warningManager.displayWarning(name='noMatch',text='Passwords do not match!')
			return

		if not machinery.CheckPassword( self.oldpass_in.get() ):

			self.app.warningManager.displayWarning(name='badPass',text='Old password incorrect!')
			return 

		newpass = self.pass_in.get()

		machinery.SaveMasterPass( newpass )
		self.app.password = newpass
		self.app.SaveData()

		self.app.ChangeState( mainMenu )

		pass

	def Cancel( self, event=None ):

		self.app.ChangeState( Settings )
		pass
