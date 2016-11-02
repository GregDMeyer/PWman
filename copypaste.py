'''
Some wrappers for copy/paste functions
'''

import Tkinter as tk

class Clipboard:

    def __init__(self, master):
        self._clip_root = master
        
        self.user_contents = self.paste()

        self.current = None
        return

    def paste(self):
        try:
            return self._clip_root.clipboard_get(type='UTF8_STRING')
        except:
            return ''

    def copy(self, data):

        if self.paste() != self.current: # the user has put something on here since we used it
            self.user_contents = self.paste()

        self._clip_root.clipboard_clear()
        self._clip_root.clipboard_append(data)
        return

    def revert(self): # get rid of whatever PWman had on the clipboard, and put back what the user had

        try:
            self._clip_root.clipboard_clear()
            self._clip_root.clipboard_append(self.user_contents if self.user_contents is not None else '')

        except:
            tmp_root = tk.Tk()
            tmp_root.withdraw()

            tmp_root.clipboard_clear()
            tmp_root.clipboard_append(self.user_contents if self.user_contents is not None else '')

        return