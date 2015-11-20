from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256
from cPickle import loads
import base64
import string

KEY_STRETCH = 25000

class AESError(Exception):

	def __init__(self, msg):

		self.msg = msg
		print self.msg
		pass


def pad(string, block_size=16):

	n_pad_chars = block_size - len(string) % block_size
	padding = n_pad_chars * chr(n_pad_chars)

	return string + padding 


def unpad(string):

	n_pad_chars = ord( string[-1] )

	return string[0:-n_pad_chars]


def encrypt(string,password):

	salt = Random.new().read( 4 )

	string = pad( string )

	for i in xrange( KEY_STRETCH - 1 ):
		h = SHA256.new()
		h.update( salt + password )
		password = h.digest()
		pass

	iv = Random.new().read( AES.block_size )

	cipher = AES.new( password, AES.MODE_CBC, iv )

	return salt + iv + cipher.encrypt( string )


def decrypt(encoded,password):

	salt = encoded [:4]

	for i in xrange( KEY_STRETCH - 1 ):
		h = SHA256.new()
		h.update( salt + password )
		password = h.digest()
		pass

	iv = encoded[4:20]

	ciphertext = encoded[20:]

	cipher = AES.new( password, AES.MODE_CBC, iv )

	decoded = cipher.decrypt( ciphertext )

	if decoded == '\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10':

		return ''

	try:
		decoded = unpad( decoded )
		loads(decoded)
	except:
		raise AESError('Bad decrypt! Corrupt data or bad password.')
		return None

	return decoded


def decryptFromFile( infile_path, password ):

	ciphertext = ''

	encfile = open( infile_path, 'r' )

	for line in encfile.readlines():
		ciphertext += line
		pass

	return decrypt( ciphertext, password )


def encryptToFile( plaintext, outfile_path, password ):

	outfile = open( outfile_path, 'w' )

	ciphertext = encrypt( plaintext, password )

	outfile.write( ciphertext )
	outfile.close()

	return 0


def checkPass(password, hashfile):

	hashed = hashfile.read()

	salt = hashed[:4]

	hashed = hashed[4:]

	for i in xrange( KEY_STRETCH + 1 ):
		h = SHA256.new()
		h.update( salt + password )
		password = h.digest()
		pass

	return hashed == password


def savePass(password,hashfile):

	salt = Random.new().read( 4 )

	for i in xrange( KEY_STRETCH + 1 ):
		h = SHA256.new()
		h.update( salt + password )
		password = h.digest()
		pass

	hashfile.write( salt + password )

	return
