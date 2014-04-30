import subprocess
import os
import sys
import time

def paste():
     p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
     retcode = p.wait()
     data = p.stdout.read()
     return data

def copy(data):
     p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
     p.stdin.write(data)
     p.stdin.close()
     retcode = p.wait()

# put data on clipboard for only 20 seconds, then revert to whatever
# used to be on the clipboard
def tempcopy(data):
	oldclip = paste()
	copy(data)
	if os.fork():
		sys.exit()

	time.sleep(20)

	copy(oldclip)