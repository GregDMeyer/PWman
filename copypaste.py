'''
Some small wrappers for the copy/paste functions for OS X.

This is I think the only part that would have to be modified to get PWman to run on linux
'''

from AppKit import NSPasteboard, NSArray, NSStringPboardType


class Clipboard:

    def __init__(self):
        self._pb = NSPasteboard.generalPasteboard()
        
        try: # PyObjC can't handle having nothing in the clipboard
            self.user_contents = self.paste() # this keeps tracks of what the user had in the clipboard before
        except AttributeError:
            self.user_contents = None

        self.current = None
        return

    def paste(self):
        return self._pb.stringForType_(NSStringPboardType).encode('ascii','ignore')

    def copy(self, data):

        if self.paste() != self.current: # the user has put something on here since we used it
            self.user_contents = self.paste()

        self._pb.clearContents()
        a = NSArray.arrayWithObject_( data )
        self._pb.writeObjects_(a)
        return

    def revert(self): # get rid of whatever PWman had on the clipboard, and put back what the user had

        self.copy( self.user_contents if self.user_contents is not None else '' )
        return