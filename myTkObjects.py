
'''
Some custom classes I wrote to make Tk buttons, lists etc. that look pretty. Mostly changes in font, colors, style, etc. 
Notably different stuff is for example the button class below, which actually is subclassed from Tkinter's Text object.
'''

import Tkinter as tk
import tkFont
import string

FONT_FAMILY = 'Avenir Light'

class myButton( tk.Text ):

    def __init__(self,
                 master,
                 text='',
                 command=None,
                 color='green',
                 disabled=False,
                 font_size=30,
                 *args,
                 **kwargs):

        tk.Text.__init__(self,master,*args,**kwargs)

        self.tag_configure("center", justify='center')
        self.insert(tk.END,text,"center")
        self.command = command
        self.disabled = disabled
        self.state = 'inactive'

        if color == 'green':
            self.bg = 'dark green'
            self.fg = 'papaya whip'
            self.active_color = 'forest green'
            self.disabled_fg = 'papaya whip'
            self.disabled_bg = 'dark sea green'

        elif color == 'gray':
            self.bg = 'gray30'
            self.fg = 'papaya whip'
            self.active_color = 'gray45'
            self.highlight = 'light sky blue'
            self.disabled_fg = 'slate gray'
            self.disabled_bg = 'gray20'

        elif color == 'light gray':
            self.bg = 'gray70'
            self.fg = 'dark slate gray'
            self.active_color = 'gray85'
            self.disabled_fg = 'slate gray'
            self.disabled_bg = 'gray78'

        elif color == 'dark blue':
            self.bg = 'navy'
            self.fg = 'light sky blue'
            self.active_color = 'RoyalBlue4'

        else:
            raise Exception(color+' is not a valid color.')

        self.config(
            font=(FONT_FAMILY,font_size),
            state='disabled', # this doesn't mean the button is disabled. it is the text object
            cursor='arrow',
            height=1,
            relief='flat',
            bd=1,
            width=20,
            pady=5,
            highlightthickness=2,
            highlightcolor=self.bg,
            highlightbackground=self.bg,
            )
        if self.disabled:
            self.config(
                bg=self.disabled_bg,
                fg=self.disabled_fg,
                )
        else:
            self.config(
                bg=self.bg,
                fg=self.fg,
                )
        self.config(*args,**kwargs)

        if not self.disabled:
            self.bind('<Enter>',self._mouse_in)
            self.bind('<Leave>',self._mouse_out)
            self.bind('<Button-1>',self._mouse_down)
            self.bind('<ButtonRelease-1>',self._mouse_up)
            pass

        self.mouse = {
            'in':False,
            'down':False
        }

        self.active = False

    def _mouse_in(self,event):

        #print 'Mouse in.'
        self.mouse['in'] = True
        self.config(bg=self.active_color,)
        if not self.active:
            self.config(highlightcolor=self.active_color,highlightbackground=self.active_color)
        if self.state == 'clicking':
            self.config(relief='sunken')
        pass

    def _mouse_out(self,event):

        #print 'Mouse out.'
        self.mouse['in'] = False
        self.config(relief='flat')
        self.config(bg=self.bg,)
        if not self.active:
            self.config(highlightcolor=self.bg,highlightbackground=self.bg)
        pass

    def _mouse_down(self,event):

        #print 'Mouse down.'
        self.mouse['down'] = True
        if self.mouse['in']:
            self.config( relief='sunken' )
            self.state = 'clicking'
            pass
        pass

    def _mouse_up(self,event):

        #print 'Mouse up.'
        self.mouse['down'] = False
        self.config(relief='flat')
        if self.mouse['in']:
            self.state = 'active'
            pass
        else:
            self.state = 'inactive'
            pass
        if self.mouse['in'] and self.command:
            self.command( event )
            pass
        pass

    def make_active(self):

        self.active = True

        self.config(highlightcolor=self.highlight)
        self.config(highlightbackground=self.highlight)
        return 

    def make_inactive(self):

        self.active = False

        self.config(highlightcolor=self.bg)
        self.config(highlightbackground=self.bg)
        return

    def disable(self):

        self.config(
                bg=self.disabled_bg,
                fg=self.disabled_fg,
                )

        self.unbind('<Enter>',)
        self.unbind('<Leave>',)
        self.unbind('<Button-1>',)
        self.unbind('<ButtonRelease-1>',)

    def enable(self):

        self.config(
                bg=self.bg,
                fg=self.fg,
                )

        self.bind('<Enter>',self._mouse_in)
        self.bind('<Leave>',self._mouse_out)
        self.bind('<Button-1>',self._mouse_down)
        self.bind('<ButtonRelease-1>',self._mouse_up)

    def replace_text(self, newtext):

        self.config(state='normal')
        self.delete(1.0,tk.END)
        self.insert(tk.END,newtext,"center")
        self.config(state='disabled')


class myEntry( tk.Frame, object ):

    def __init__(self,master,text='',password=False,showable=False,*args,**kwargs):

        tk.Frame.__init__(self,master,*args,**kwargs)

        self.password = password
        self.showable = showable
        if showable and not password:
            raise Exception('Showable entry, but not a password? wat')
        self.show = False

        self.entry = tk.Entry(self)

        self.bg='light sky blue'

        self.entry.config(
            font=(FONT_FAMILY,30),
            width=18 if showable else 20,
            relief='flat',
            bg=self.bg,
            highlightthickness=2,
            highlightcolor=self.bg,
            highlightbackground=self.bg,
            fg='dodger blue',
            )

        self.entry.pack(ipady=5,side='left' if showable else 'top',fill=tk.NONE if showable else 'x')

        if self.showable: # put the button to toggle show or not
            self.togglebutton = myButton(self,width='2',text='a',command=self._toggle_show,color='dark blue')
            self.togglebutton.pack(side='right',fill='y')

        self.text = text
        self.empty = True
        self.entry.insert(tk.END,self.text)

        self.entry.bind('<FocusIn>', self._focus_in )
        self.entry.bind('<FocusOut>', self._focus_out )

        # these are set with bind later
        self.focus_in_cmd = lambda: None
        self.focus_out_cmd = lambda: None
        return


    def _focus_in( self, event ):

        self.focus_in_cmd()

        if self.empty:
            self.entry.delete(0,tk.END)
            self.entry.config(fg='navy')
            if self.password and not self.show:
                self.entry.config(show='*')
                pass
            self.empty = False

        return


    def _focus_out( self, event ):

        self.focus_out_cmd()

        if not self.get():
            self.empty = True
            self.entry.config(show='',fg='dodger blue')
            self.entry.insert(tk.END,self.text)

        else:
            self.empty = False
        
        return


    # this should only be called if password and showable are both true
    def _toggle_show(self,event):

        if self.togglebutton.get(1.0,tk.END).strip() == 'a':
            self.entry.config(show='')
            self.show = True
            self.togglebutton.replace_text('*')

        else:
            if not self.empty:
                self.entry.config(show='*')
            self.show = False
            self.togglebutton.replace_text('a')
        return


    def get(self,*args,**kwargs):

        if self.empty:
            return ''
        else:
            return self.entry.get(*args,**kwargs)
            pass


    def set(self, val):

        self.entry.delete(0,tk.END)
        self.entry.insert(tk.END,val)
        self.entry.config(fg='navy')

        if self.password and not self.show:
            self.entry.config(show='*')

        self.empty = False
        return


    def bind(self,*args,**kwargs):

        if '<FocusIn>' in args or '<FocusOut>' in args:
            self._bind(*args,**kwargs)
        else:
            self.entry.bind(*args,**kwargs)
        return


    def _bind(self, *args, **kwargs):

        if args[0] == '<FocusIn>':
            self.focus_in_cmd = args[1]
        elif args[0] == '<FocusOut>':
            self.focus_out_cmd = args[1]
        return


    def focus_insert(self, char):

        self.entry.focus_set()

        self.entry.delete(0,tk.END)
        self.entry.config(fg='navy')

        if self.password and not self.show:
            self.entry.config(show='*')

        self.empty = False
        self.entry.insert(tk.END, char)

        self.entry.bind('<FocusIn>', self._focus_in )

        return


    def clear(self):
        self.entry.delete(0,tk.END)
        return


class myTitle( tk.Text ):

    def __init__(self,master,text='',**options):

        tk.Text.__init__(self,master,**options)

        self.tag_configure("center", justify='center')
        self.insert(tk.END,text,"center")

        self.bg='old lace'

        self.config(
            font=(FONT_FAMILY,30),
            state='disabled',
            cursor='arrow',
            height=1,
            relief='flat',
            bd=1,
            width=20,
            pady=10,
            bg='old lace',
            highlightthickness=2,
            highlightcolor=self.bg,
            highlightbackground=self.bg,
            fg='OrangeRed4',
            )


class myMessage( tk.Text, object ):

    def __init__(self,master,text='',*args,**kwargs):

        tk.Text.__init__(self,master,*args,**kwargs)

        self.tag_configure("center", justify='center')
        self.insert(tk.END,text,"center")

        self.bg='old lace'

        self.config(
            font=(FONT_FAMILY,15),
            state='disabled',
            cursor='arrow',
            relief='flat',
            bd=1,
            height=1,
            width=30,
            bg='old lace',
            highlightthickness=2,
            highlightcolor=self.bg,
            highlightbackground=self.bg,
            fg='OrangeRed4',
            )
        self.config(*args,**kwargs)

    def pack( self,*args,**kwargs ):

        if 'fill' not in kwargs.keys():
            kwargs[ 'fill' ] = 'x'

        super(myMessage,self).pack(*args,**kwargs)


class myDoubleButton( tk.Frame, object):

    def __init__(self, 
                 master, 
                 left_text='', 
                 right_text='', 
                 left_command=None, 
                 right_command=None, 
                 left_disabled=True, 
                 right_disabled=False, 
                 width=20):

        self.master = master
        tk.Frame.__init__(self, self.master, borderwidth=0) # this is only OK for light gray... yeah

        color='light gray'

        self.left_button = myButton(self, width=width/2, color=color, text=left_text, command=left_command, highlightthickness=0, bd=1, disabled=left_disabled)
        self.left_button.pack(side='left',fill='x',expand=True)

        self.right_button = myButton(self, width=width/2, color=color, text=right_text, command=right_command, highlightthickness=0, bd=1, disabled=right_disabled)
        self.right_button.pack(side='left',fill='x',expand=True)

        return

    def set_left_disabled(self, val = True):

        if val:
            self.left_button.disable()
        else:
            self.left_button.enable()
        return

    def set_right_disabled(self, val = True):

        if val:
            self.right_button.disable()
        else:
            self.right_button.enable()
        return



class myPageList( tk.Frame, object):

    def __init__(self, 
                 master, 
                 name_list, 
                 selection_change_fn=lambda: None, 
                 width=20):

        self.master = master
        self.selection_change_fn = selection_change_fn

        tk.Frame.__init__(self, self.master)

        self.visible_index = 0

        self.full_name_list = name_list
        self.name_list = name_list

        self.buttons = []
        self.selection = None
        self.filter = ''

        # bind all keys to filter

        for char in string.ascii_letters+string.digits+string.punctuation:
            if char == '<':
                char = '<less>'
                pass
            self.bind_all(char, self.key_pressed)
            pass

        self.bind_all('<space>', self.key_pressed)
        self.bind_all('<BackSpace>', self.BS_pressed)

        # display buttons. We will only change names and colors after this, not repack them (that way it doesn't look jumpy)
        for i in xrange(5):
            self.buttons.append( myButton( self , text='', command=self.choice_made, color='gray' ) )
            self.buttons[-1].pack(fill='x')

        if len( self.full_name_list ) > 5:
            self.more_button = myDoubleButton(
                self, 
                left_text='< BACK', 
                right_text='MORE >', 
                left_command=self.back_choices,
                right_command=self.next_choices,
                left_disabled = True
                )
            self.more_button.pack(side='bottom',fill='x')

        self.display_list()
        return


    def BS_pressed(self,event):

        self.selection = None

        for button in self.buttons:
            button.make_inactive()

        if self.filter:
            self.visible_index = 0

        self.filter = self.filter[:-1]

        self.name_list = [x for x in self.full_name_list if self.filter.lower() in x.lower()]

        self.display_list()
        return


    def key_pressed(self,event):

        self.selection = None

        for button in self.buttons:
            button.make_inactive()
            pass

        # don't keep adding letters if there is nothing left of the list!
        if not self.name_list:
            return

        self.filter += event.char

        self.name_list = [x for x in self.full_name_list if self.filter.lower() in x.lower()]

        self.visible_index = 0

        self.display_list()

        return


    def display_list(self):

        for button in self.buttons:
            button.make_inactive()
            pass

        active_cutoff = min(5,len(self.name_list) - self.visible_index)

        for i in xrange(active_cutoff):
            self.buttons[i].enable()
            self.buttons[i].replace_text(self.name_list[self.visible_index + i])

        for i in xrange( active_cutoff, 5 ):
            self.buttons[i].disable()
            self.buttons[i].replace_text('')

        if len(self.full_name_list) > 5: # disable/enable page buttons
            self.more_button.set_left_disabled( self.visible_index == 0 )
            self.more_button.set_right_disabled( self.visible_index+5 >= len( self.name_list ) )

        return


    def next_choices(self, event):

        if self.visible_index + 5 >= len(self.name_list):
            return

        self.visible_index += 5
        self.selection_change_fn()
        self.selection = None
        self.display_list()

        return


    def back_choices(self, event):

        if self.visible_index == 0:
                return

        self.visible_index -= 5
        self.visible_index = max(self.visible_index, 0)

        self.selection_change_fn()
        self.selection = None
        self.display_list()

        return


    def choice_made( self, event):

        self.selection = event.widget.get(1.0,tk.END).strip()

        for button in self.buttons:
            button.make_inactive()
            
        event.widget.make_active()
        self.selection_change_fn()
        return


    def set_selection( self, index ):

        button = self.buttons[ index ]
        self.selection = button.get(1.0,tk.END).strip()

        for button in self.buttons:
            button.make_inactive()
            
        button.make_active()
        self.selection_change_fn()
        return


    def get_selection( self ):
        return self.selection


    def destroy( self ): # clean up nicely (though whenever this is destroyed, change_state should unbind stuff anyway)

        for char in string.ascii_letters+string.digits+string.punctuation:
            if char == '<':
                char = '<less>'
                pass
            self.unbind_all(char)
            pass

        self.unbind_all('<space>')
        self.unbind_all('<BackSpace>')

        super(myPageList,self).destroy()

        return



class myWarningManager( tk.Frame, object ):

    def __init__(self, master):

        self.master = master
        tk.Frame.__init__(self,self.master,height=0)
        self.warnings = {}

        return

    # show a new warning
    def display_warning(self, name, text):

        # if this one already exists, it is cleared and replaced.
        if name in self.warnings.keys():
            self.warnings[ name ].pack_forget()
            self.warnings[ name ].destroy()
            pass

        self.warnings[ name ] = myMessage( self, text = text, height = text.count('\n')+1)
        self.warnings[ name ].pack(fill='x')

        # make sure the manager is packed as well.
        # if you pack the manager with no warnings in it, it shows up as a 1-pixel wide line :(
        # that's why you have to do this shenanigans instead of packing it right away.
        if not self.winfo_ismapped():
            self._pack()
            pass

        return

    # clear warning with name 'name'
    def clear(self, name):

        if not name in self.warnings.keys():
            raise Exception('There is no warning with name \''+name+'\'.')

        self.warnings[ name ].pack_forget()
        self.warnings[ name ].destroy()

        self.warnings.pop( name )

        # no more - clear the manager as well
        if not self.warnings:
            self.pack_forget()

        return


    # try to clear warning with name 'name', if it doesn't exist, that's fine.
    def try_clear(self, name):

        if not name in self.warnings.keys():
            return

        self.warnings[ name ].pack_forget()
        self.warnings[ name ].destroy()

        self.warnings.pop( name )

        if not self.warnings:
            self.pack_forget()
        
        return


    # clear all warnings present.
    def clear_all(self):

        for child in self.winfo_children():
            child.pack_forget()
            child.destroy()

        self.warnings = {}

        self.pack_forget()
        return

    # this is what is called when we actually need to pack the warning manager, 
    # instead of hiding it
    def _pack(self):
        if self.packed:
            super(myWarningManager,self).pack(*self.pack_args,**self.pack_kwargs)
        return

    # this is to "pack" the larger warning manager class
    def pack(self,*args,**kwargs):

        self.pack_args = args
        self.pack_kwargs = kwargs

        self.packed = True
        return

