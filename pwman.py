#! /usr/bin/env python

import os
import sys
import errno
import hashlib
from getpass import getpass
from os.path import expanduser, isfile
home = expanduser("~") # get the address of the user's home directory
import aes # make sure that aes and copypaste are in the right spot!
import copypaste

args = sys.argv[1:] #get a list of the arguments, without the original function name

# see if the directory is there, if not, make it
def check_or_make_dir(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
			pass
		pass
	pass

# ask for a new password to store from the user
def GetNewPasswd( service=False, keys=[], new=True ):

	if not service: # no service provided
		service = raw_input('What is the name of the service this password is for? ')
		pass

	if not new and not service in keys: 	# they want to change a password that doesn't exist!
		query = raw_input('You don\'t have anything saved for \''+service+'\'. \nWould you like to save a password for it? ')
		if not query in ['y','Y','yes']:
			sys.exit()
			pass
		pass

	if new and service in keys: 	# they want to make a password that already exists!
		query = raw_input('You already have a password saved for \''+service+'\'. \nWould you like to change it? ')
		if not query in ['y','Y','yes']:
			sys.exit()
			pass
		pass

	newpass = getpass('Password for service \''+service+'\': ')
	return {service: newpass}

#turn the data in the dictionary into a string to be encoded and stored to drive
def makeString(dataDict):
	outstring = ''
	for serv, passwd in dataDict.iteritems():
		outstring += serv+'\n'+passwd+'\n,\n'
		pass
	return outstring

# what arguments are OK?
valid_args = ['new','change','update','get','list','reset','change-master-password','remove']

#print usage if user is doing it wrong
if not any(x in valid_args for x in args) and os.path.exists(home+'/.pwman_test'):
	usage = ''' 
USAGE: pwman [option]

	A simple password manager for command line.

OPTIONS

	get [service] - temporarily copy the password for 'service' to the clipboard.

	list - list all services for which passwords have been saved, and then possibly choose one.

	new - save a new password for a service.

	change-master-password - change the master password for the manager.

	reset - delete master password and all saved passwords.

	change [service] - change the password for a service.

	update [service] - (equivalent to change)

	remove [service] - remove a password.
'''

	print usage
	sys.exit()
	pass

# see whether it's their first time!
setup = not os.path.exists(home+'/.pwman_test')

# make sure the directory exists
check_or_make_dir(home+'/.pwman_test')

# see if a password has been set. if it has been set, check it,
# otherwise ask the user for one. If somebody deletes the password
# file to try to get by this, that's fine... the decryption later
# won't work with the wrong password. This is just really to make 
# it easier for the user to be sure they have the right one.
if isfile(home+'/.pwman_test/passwd'):
	hashfile = open(home+'/.pwman_test/passwd','r')
	hashed = hashfile.read()
	string = ''
	while True:
		string = getpass('Password: ')
		if hashed == hashlib.md5(string).digest():
			break
			pass
		else:
			print 'Incorrect password. Try again...'
			pass
		pass
	pass
else:
	while True:
		string = getpass('Make new master password: ')
		string2 = getpass('Type it again: ')
		if string == string2:
			break
		print "Passwords do not match! Try again..."
		pass
	passout = open(home+'/.pwman_test/passwd','w')
	passout.write( hashlib.md5(string).digest() )
	passout.close()

nodata = False
modified = False

# see whether there are any passwords stored
if isfile(home+'/.pwman_test/data'):
	datastring = aes.decrypt(home+'/.pwman_test/data',string)
	if not datastring.strip() == '':
			data = dict( (service.strip(), passwd.strip()) for service,passwd in (item.split('\n') for item in datastring.split('\n,\n')[:-1]))
	else:
		nodata=True
else:
	nodata = True

# what to run if it is their first time running pwman
if setup:
	query = raw_input('No passwords saved. Would you like to input a new one? ')
	if query in ['y','Y','yes']:
		data = GetNewPasswd()
		modified = True
		pass
	pass
elif nodata:
	data = {}
	pass

# see if a service name was included in the command line
argService = False
if len(args) > 1:
	argService = args[1]
	pass

# turns out they can all be implemented the same way 
# with the dict.update method
if 'new' in args:
	data.update( GetNewPasswd( service=argService, keys=data.keys(), new=True ) )
	modified = True
	pass

if any(x in ['change','update'] for x in args):
	data.update( GetNewPasswd( service=argService, keys=data.keys(), new=False ) )
	modified = True
	pass

# if the user is requesting a password
elif 'get' in args:
	if not argService: # if they didn't already specify a service, get it
		service = raw_input('What service\'s password do you want? ')
		pass
	else:
		service = argService #otherwise it was specified on command line
		pass
	if service in data: # see whether there is a password saved, if so, copy it termporarily!
		copypaste.tempcopy( data[ service ] )
		pass
	else: # no dice
		print "No password saved for service",service
		pass
	pass

# list out the services for which passwords are saved
elif 'list' in args: 
	if nodata:
		print 'You have no saved passwords.'
	else:
		print '\nYou have passwords saved for: \n'
		for key in data.keys():
			print key
			pass
		# maybe they want one now that they see the list?
		req_key = raw_input('\nWhich one would you like? (\'exit\' to exit) ')
		while not (req_key in data.keys() or req_key == 'exit'):
			req_key = raw_input('That is not a valid response. Type a service name or \'exit\': ')
			pass
		# I guess they didn't want one
		if req_key == 'exit':
			sys.exit()
		# ... or they did
		else:
			copypaste.tempcopy( data[req_key] )
		pass
	pass

# get rid of everything. really mostly useful for debugging puposes, but I guess
# might be useful for a user somehow
elif 'reset' in args:
	query = raw_input('Are you sure you want to delete all data? ')
	if query in ['y','Y','yes']:
		query2 = raw_input('... really sure? ')
		if query2 in ['y','Y','yes']:
			os.remove(home+'/.pwman_test/data')
			os.remove(home+'/.pwman_test/passwd')
			pass
		pass
	pass

# change the password used for encrypting data (and entering pwman)
elif 'change-master-password' in args:
	while True:
		string = getpass('New master password: ')
		string2 = getpass('Type it again: ')
		if string == string2:
			break
		print "Passwords do not match! Try again..."
		pass
	passout = open(home+'/.pwman_test/passwd','w')
	passout.write( hashlib.md5(string).digest() )
	passout.close()
	modified = True
	print "Successfully changed master password."
	pass

# delete a saved password
elif 'remove' in args:
	if not argService:
		service = raw_input('Name of service to be removed: ')
		pass
	else:
		service = argService
		pass

	# make sure the input is valid
	while not (service in data.keys() or service == 'exit'):
		service = raw_input('You don\'t have a password saved for '+service+'. \nRetry or type \'exit\' to exit: ')
		pass
	if service == 'exit':
		sys.exit()
		pass

	query = raw_input('Are you sure you want to remove \''+service+'\'? ')
	if query in ['y','Y','yes']:
		query2 = raw_input('... really sure? ')
		if query2 in ['y','Y','yes']:
			del data[ service ]
			modified = True
			pass
		else:
			print 'OK. No changes made.'
			pass
		pass
	else:
		print 'OK. No changes made.'
		pass
	pass

# check if we need to modify the saved datafile. if so, re-encrypt and rewrite it.
if modified:
	outstring = makeString( data )
	aes.encrypt(outstring,home+'/.pwman_test/data',string)
