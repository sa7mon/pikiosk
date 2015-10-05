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

# readFile
# Reads a file into a dictionary
# File needs to be in key=value format
def readFile(file):
        readDict = {}
        with open(file, "r") as text:
                for line in text:
                        # For each line in the test file, do the following
            		# Split the line into 2 lines delimited by the equal sign
            		# Make the first string the dict key and the second the dict value
                        readDict[line.split('=', 2)[0]] = line.split('=', 2)[1].strip('\n')
                #print readDict # DEBUG
        return readDict

##################   MAIN PROGRAM   ####################### 

# Read the file with videos and tag IDs into a dict
print "Reading videos file..."
videoDict = readFile("videos.txt")

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

