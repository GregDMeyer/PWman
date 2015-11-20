
import os
import errno
from os.path import isfile
import aes # make sure that aes and copypaste are in the right spot!
import copypaste
import cPickle

from Cocoa import NSHomeDirectory
home = NSHomeDirectory()


def FirstTime():
	return not isfile(home+'/.pwman_test/passwd')

def CheckPassword( password ):
	hashfile = open(home+'/.pwman_test/passwd','r')
	result = aes.checkPass(password, hashfile)
	hashfile.close()
	return result

def SaveMasterPass( password ):

	check_or_make_dir( home+'/.pwman_test/' )
	passout = open(home+'/.pwman_test/passwd','w')

	aes.savePass(password,passout)

	passout.close()
	return

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

def GetData( password ):
	nodata = False

	# see whether there are any passwords stored
	if isfile(home+'/.pwman_test/data'):
		datastring = aes.decryptFromFile(home+'/.pwman_test/data',password)
		if not datastring.strip() == '':
			data = cPickle.loads( datastring )
		else:
			data = {}
	else:
		data = {}

	return data

def CopyPass( password ):
	copypaste.copy( password )
	pass

def WriteFile( data, password ):
	outstring = cPickle.dumps( data )
	aes.encryptToFile(outstring,home+'/.pwman_test/data',password)
