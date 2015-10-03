#!/usr/bin/env python
#
# Written by: Dan Salmon
# Created on: 10/02/15 
#
import nfc 

#IDtoVideo
def idToVid(id):
    videolookup = (
		   ("04C023D24C2880", "video1"), 
		   ("048D495A002980", "video2"), 
		   ("3", "video3")
		  )
    videolookup2 = ("04C023D24C2880:video1", "048D495A002980:video2")
    
    # Loop through the array, checking each item to see if it starts with the ID we were given.
    for entry in videolookup2:
        # Do something
	entryid = entry.split(":", 2)[0] # Should give us just the string before the colon
	entryvideo = entry.split(":", 2)[1]
	print "entryid: ", entryid # DEBUG
	print "entryvideo: ", entryvideo # DEBUG

    return

# printTag
# function that gets the id we need. Runs only when on-connect event is raised.
def printTag(tag):
    # We're only interested in the ID. 
    tagID = str(tag).split("ID=", 1)[1]
    print tagID
    print idToVid(id)
    return

print "Initiating reader..."
# Setup our reader connection through UART
# To verify from Python CLI, print(clf) should result in /dev/AMA0
clf = nfc.ContactlessFrontend('tty')

loop = 1;
# Continuously listen for tags nearby. Fire an event when we see one.
while loop == 1: 
    print "Waiting for tag to read..."
    clf.connect(rdwr={'on-connect': printTag})
