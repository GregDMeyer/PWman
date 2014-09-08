from AppKit import NSPasteboard, NSArray, NSStringPboardType

pb = NSPasteboard.generalPasteboard()

def paste():
     return pb.stringForType_(NSStringPboardType).encode('ascii','ignore')

def copy(data):
     pb.clearContents()
     a = NSArray.arrayWithObject_( data )
     pb.writeObjects_(a)
     return

# put data on clipboard for only 20 seconds, then revert to whatever
# used to be on the clipboard
def tempcopy(data):
	oldclip = paste()
	copy(data)
	if os.fork():
		sys.exit()

	time.sleep(20)

	copy(oldclip)