#!/usr/bin/env python
#####
# Created by: Dan Salmon
# Created on: 10/8/15
#####

################   IMPORTS   #################
import nfc 

################  FUNCTIONS  #################

# printTag
# function that gets the id we need. Runs only when on-connect event is raised.
def printTag(tag):
    # We're only interested in the ID. 
    tagID = str(tag).split("ID=", 1)[1]
    print "Tag ID: ", tagID, "\n"
    return

def readTag():
    # Continuously listen for tags nearby. Fire an event when we see one.
    # Make loop not 1 if loop needs to break
    waitingForTag = 1
    while waitingForTag == 1: 
        print "Waiting for tag to read..."
        clf.connect(rdwr={'on-connect': printTag})
        
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
    
    quit = False
    
    while quit == False:
        # Loop through menu here
        menu = "1. Read a tag's ID\n2. Quit"
        print menu
        
        userInput = raw_input("Enter a choice: ")
        
        if userInput == "1":
            print "Waiting for tag..."
            clf.connect(rdwr={'on-connect': printTag})
        elif userInput == "2":
            quit = True
        else:
            print "Not a valid choice. Please try again."
        
    # User has chosen to quit if you get here.
    print "Goodbye!"