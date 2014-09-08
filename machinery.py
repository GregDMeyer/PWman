#! /usr/bin/env python

import os
import sys
import time
import errno
import hashlib
from getpass import getpass
from os.path import expanduser, isfile
import aes # make sure that aes and copypaste are in the right spot!
import copypaste
import cPickle
from Tkinter import *
from Crypto import Random

from Cocoa import NSHomeDirectory
home = NSHomeDirectory()


KEY_STRETCH = 50000


def FirstTime():

	return not isfile(home+'/.pwman_test/passwd')

def CheckPassword( password ):

	hashfile = open(home+'/.pwman_test/passwd','r')

	hashed = hashfile.read()

	salt = hashed[:4]

	hashed = hashed[4:]

	for i in xrange( KEY_STRETCH + 1 ):
		password = hashlib.md5( salt + password ).digest()
		pass

	return hashed == password

def SaveMasterPass( password ):

	check_or_make_dir( home+'/.pwman_test/' )
	passout = open(home+'/.pwman_test/passwd','w')

	salt = Random.new().read( 4 )

	for i in xrange( KEY_STRETCH + 1 ):
		password = hashlib.md5( salt + password ).digest()
		pass

	passout.write( salt + password )
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

def CopyPass( password, time ):
	copypaste.copy( password )
	pass

def WriteFile( data, password ):
	outstring = cPickle.dumps( data )
	aes.encryptToFile(outstring,home+'/.pwman_test/data',password)
	print 'Data saved.'
