'''
Some small wrappers for the copy/paste functions for OS X.

This is I think the only part that would have to be modified to get PWman to run on linux
'''

from AppKit import NSPasteboard, NSArray, NSStringPboardType

pb = NSPasteboard.generalPasteboard()

def paste():
     return pb.stringForType_(NSStringPboardType).encode('ascii','ignore')

def copy(data):
     pb.clearContents()
     a = NSArray.arrayWithObject_( data )
     pb.writeObjects_(a)
     return