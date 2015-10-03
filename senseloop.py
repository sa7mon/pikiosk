#!/usr/bin/env python
#
# Written by: Dan Salmon
# Created on: 10/02/15 
#
import nfc 

#IDtoVideo
def idToVid(id):
    videolookup = ((1, "video1"), (2, "video2"), (3, "video3"))
    return

# printTag
# function that gets the id we need. Runs only when on-connect event is raised.
def printTag(tag):
    # We're only interested in the ID. 
    tagID = str(tag).split("ID=", 1)[1]
    print tagID
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
