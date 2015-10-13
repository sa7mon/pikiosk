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

def closeReader():
	# Close the reader
	#nfc.closeReader(clf)
	# Then set loop to not 1 to cleanly exit program instead of suspending it.
	global loop 
	loop = 0
	return

# idToVid
# Takes a tag ID and checks it against an array of arrays with items set up as:
# (tagID, video) and returns the video.
def idToVid(id):
    # Give the return variable a default value of error.
    # Hopefully, this doesn't get returned.

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
#
# file data needs to be in 'key=video=color' format
# mode can be either "videos" or "lights"
def readFile(file, mode):
	# Initialize a blank dictionary to fill and then return
	readDict = {}
	
	# Check to make sure the mode passed is one of the approved 2
	if not ((mode == "videos") or (mode == "lights")):
		print "Error: read(): Bad mode passed"
		return readDict
	
	# Open the file as text
	with open(file, "r") as text:
		# For each line in the test file, do the following
            	# Split the line into 2 lines delimited by the equal sign
            	# Make the first string the dict key and the second the dict value
		for line in text:
			if (mode == "videos"):
				readDict[line.split('=', 2)[0]] = line.split('=', 2)[1].strip('\n')
			elif (mode == "lights"):
				readDict[line.split('=', 3)[0]] = line.split('=', 3)[2].strip('\n')
	return readDict 

##################   MAIN PROGRAM   ####################### 

# Read the file with videos and tag IDs into a dict
print "Reading videos file..."
videoDict = readFile("videoscolors.txt", "videos")
lightsColorsDict = readFile("videoscolors.txt", "lights")

#DEBUG
print videoDict
print lightsColorsDict


# Setup our reader connection through UART
# To verify from Python CLI, print(clf) should result in /dev/AMA0

'''
print "Initiating reader..."
try:
    clf = nfc.ContactlessFrontend('tty')
except IOError:
    print "Couldn't initialize reader (IOError)"
else: 
    
    # Continuously listen for tags nearby. Fire an event when we see one.
    # Make loop not 1 if loop needs to break
    loop = 1; 
    while loop == 1: 
        print "Waiting for tag to read..."
        clf.connect(rdwr={'on-connect': printTag})
'''

