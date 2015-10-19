#!/usr/bin/env python

#################################
#
# Written by: Dan Salmon
# Created on: 10/02/15 
#
#################################

################   IMPORTS   #################
import sys
sys.path.append("/home/osmc/Scripts/nfcpy/trunk/")
import nfc 

###############   FUNCTIONS  #################

def closeReader():
	global clf
	global loop 

	# Close the reader
	clf.close()

	# Then set loop to not 1 to cleanly exit program instead of suspending it.
	loop = 0
	return

def on_connect(tag):
    global loop
    global videoDict
    global lightsColorsDict
    
    # Get the tag's ID 
    tagID = str(tag).split("ID=", 1)[1]

    # Check if the tag exists in both dictionaries
    if not ((tagID in videoDict) and (tagID in lightsColorsDict)):
        print "This tag doesn't exist in one of the dictionaries."
    	
    #Get video to play
    video = videoDict.get(tagID)
    
    print video
	
    return

def readFile(file, mode):
	# readFile - Reads a file into a dictionary
	#
	# file data needs to be in 'key=video=color' format
	# mode can be either "videos" or "lights"

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

################# VARIABLES #######################

# Our flag to keep looping later
loop = 1

# The folder containing all the videos to play
dirVideos = "/home/osmc/Movies/"

# The text file containing our video names, tagIDs, and light colors
fileVideos = "videos.txt"


##################   MAIN PROGRAM   ####################### 

# Read the file with videos and tag IDs into a dict
print "Reading videos file..."
videoDict = readFile(fileVideos, "videos")
lightsColorsDict = readFile(fileVideos, "lights")


# Setup our reader connection through UART
# To verify from Python CLI, print(clf) should result in /dev/AMA0
# Alternately, 'tty:AMA0:pn532' will probably work in place of 'tty'
print "Initiating reader..."
try:
    clf = nfc.ContactlessFrontend('tty')
except IOError:
    print "Couldn't initialize reader (IOError)"
else: 
    
    # Continuously listen for tags nearby. Fire an event when we see one.
    # Make loop not 1 if loop needs to break
    while loop == 1: 
        print "Waiting for tag to read..."
        clf.connect(rdwr={'on-connect': on_connect})
	closeReader()
