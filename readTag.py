#!/usr/bin/env python

######################################################################
# Created by: Dan Salmon
# Created on: 10/8/15
#
# readTag.py - Simple script made so videos.txt can be updated later by a non-technical
#              individual. Run the script, scan a tag and it will give you the
#              tag's ID. Script should be placed on Desktop or shortcut created.
#######################################################################


################   IMPORTS   #################
import sys
sys.path.append("/home/osmc/Scripts/nfcpy/trunk/")
import nfc 

################  FUNCTIONS  #################

# printTag
# function that gets the id we need. Runs only when on-connect event is raised.
def printTag(tag):
    # We're only interested in the ID. 
    tagID = str(tag).split("ID=", 1)[1]
    print "Tag ID: ", tagID, "\n"
    return

############## MAIN PROGRAM  #################

# Setup our reader connection through UART
# To verify from Python CLI, print(clf) should result in /dev/AMA0
print "Initiating reader..."
try:
    clf = nfc.ContactlessFrontend('tty')
    print "Reader initiated.\n" #DEBUG?
except IOError:
    print "Couldn't initialize reader (IOError)"
else: 
    # Set loop flag to False. Change to anything else to exit menu loop.
    quit = False
    
    while quit == False:
        # Loop through menu here
        menu = "1. Read a tag's ID\n2. Quit"
        print menu
        
        userInput = raw_input("Enter a choice: ")
        
        if userInput == "1":
            print "Waiting for tag..."
            
            # Set function to fire on on-connect event.
            # http://nfcpy.org/latest/topics/get-started.html#read-and-write-tags
            clf.connect(rdwr={'on-connect': printTag})
        elif userInput == "2":
            # Set loop flag to not-false to exit menu loop.
            quit = True
        else:
            print "Not a valid choice. Please try again."
        
    # User has chosen to quit if you get here.
    print "Goodbye!"