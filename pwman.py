import os
import sys
import errno
import hashlib
from getpass import getpass
from os.path import expanduser, isfile
home = expanduser("~") # get the address of the user's home directory
import aes #make sure that aes is in the right spot!
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
def GetNewPasswd():
	service = raw_input('What is the name of the service this password is for? ')
	newpass = getpass('Password: ')
	return {service: newpass}

def makeString(dataDict):
	outstring = ''
	for serv, passwd in dataDict.iteritems():
		outstring += serv+'\n'+passwd+'\n,\n'
		pass
	return outstring

#make sure the directory exists
check_or_make_dir(home+'/.pwman')

# see if a password has been set. if it has been set, check it,
# otherwise ask the user for one. If somebody deletes the password
# file to try to get by this, that's fine... the decryption later
# won't work with the wrong password. This is just really to make 
# it easier for the user to be sure they have the right one.
if isfile(home+'/.pwman/passwd'):
	hashfile = open(home+'/.pwman/passwd','r')
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
	string = getpass('Make new password: ')
	passout = open(home+'/.pwman/passwd','w')
	passout.write( hashlib.md5(string).digest() )
	passout.close()

nodata = False
modified = False
origdata = {}

if isfile(home+'/.pwman/data'):
	datastring = aes.decrypt(home+'/.pwman/data',string)
	if not datastring.strip() == '':
			data = dict( (service.strip(), passwd.strip()) for service,passwd in (item.split('\n') for item in datastring.split('\n,\n')[:-1]))
	else:
		nodata=True
else:
	nodata = True

if nodata:
	query = raw_input('No passwords saved. Would you like to input a new one? ')
	if query in ['y','Y','yes']:
		data = GetNewPasswd()
		modified = True
		pass
	pass

if '--new' in args:
	data.update( GetNewPasswd() )
	modified = True
	pass
elif '--get' in args:
	if (len(args) >= args.index('--get') + 2) and args[ args.index('--get') + 1 ] in data:
		copypaste.copy( data[ args[ args.index('--get') + 1 ] ] )
		pass
	else:
		print "No password saved for service",args[1]
		pass
elif '--find' in args:
	#list services, can choose
	pass
elif '--reset' in args:
	query = raw_input('Are you sure you want to delete all data? ')
	if query in ['y','Y','yes']:
		query2 = raw_input('... really sure? ')
		if query2 in ['y','Y','yes']:
			os.remove(home+'/.pwman/data')
			os.remove(home+'/.pwman/passwd')
			pass
		pass
	pass

if modified:
	outstring = makeString( data )
	aes.encrypt(outstring,home+'/.pwman/data',string)
