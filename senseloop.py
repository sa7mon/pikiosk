#!/usr/bin/env python

####
#
# Written by: Dan Salmon
# Created on: 10/02/15 
#
####

################   IMPORTS   #################
import nfc 

###############   FUNCTIONS  #################

# idToVid
# Takes a tag ID and checks it against an array of arrays with items set up as:
# (tagID, video) and returns the video.
def idToVid(id):
    # Give the return variable a default value of error.
    # Hopefully, this doesn't get returned.
    video = "unknown"
    videos = (
		   ("04C023D24C2880", "video1"), 
		   ("048D495A002980", "video2"), 
		   ("3", "video3")
		  )
    # Loop through the array, checking the first item (0) of the sub-array
    # If it matches, return the second item (1)
    for entry in videos:
	    if (entry[0] == id):
               video = entry[1]
    return video

# printTag
# function that gets the id we need. Runs only when on-connect event is raised.
def printTag(tag):
    # We're only interested in the ID. 
    tagID = str(tag).split("ID=", 1)[1]
    print "Tag ID: ", tagID
    print "Video: ", idToVid(tagID)
    return

##################   MAIN PROGRAM   ####################### 

# Setup our reader connection through UART
# To verify from Python CLI, print(clf) should result in /dev/AMA0
print "Initiating reader..."
try:
    clf = nfc.ContactlessFrontend('tto')
except IOError:
    print "Couldn't initialize reader (IOError)"
else: 
    
    # Continuously listen for tags nearby. Fire an event when we see one.
    # Make loop not 1 if loop needs to break
    loop = 1; 
    while loop == 1: 
        print "Waiting for tag to read..."
        clf.connect(rdwr={'on-connect': printTag})

