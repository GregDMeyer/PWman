import subprocess

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