PWman
=====

a simple command line password manager

This is a simple utility written in Python which stores passwords for various services so that the user can get them later if they forget.  This allows users to keep track of different passwords even for services that they rarely use. There is a master password that allows the user to access pwman, and after entering the master password the user can access any of the passwords he or she has saved.

When a password is accessed, it doesn't show up in stdout. Instead, it is copied to the clipboard for 20 seconds, after which time it is overwritten by whatever was on the clipboard before.

All passwords are saved under aes-256 encryption, with the master password needed to decrypt them.

Note - this utility will only work on Mac. A Linux version can be seen at GregDMeyer/PWman_linux.

----

INSTALLING

Copy all three files (pwman.py, aes.py, and copypaste.py) into the same directory. Then navigate to that directory and type:

~~~~
chmod +x pwman.py
ln -s /path/to/pwman.py /usr/local/bin/pwman
~~~~

where /path/to/pwman.py is the FULL path to the file. You CAN'T do something like ~/pwman/pwman.py. It won't work.

Now you should be able to simply type 'pwman' into the command line and the utility will run.

Alternatively, the utility can be run easily by going to the directory containing it and typing the command:

~~~~
./pwman.py
~~~~

You probably will need to do 

~~~~
chmod +x pyman.py
~~~~

first so that it is executable, or else it will give an error.
