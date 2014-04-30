import subprocess

def encrypt(string,outfile,password):
	p = subprocess.Popen(['openssl','aes-256-cbc','-out',outfile,'-pass','stdin'], stdin=subprocess.PIPE)
	p.communicate(password+'\n'+string)
	retcode = p.wait()

def decrypt(infile,password):
	p = subprocess.Popen(['openssl','aes-256-cbc','-d','-in',infile,'-pass','stdin'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	out = p.communicate(password)[0]
	return out