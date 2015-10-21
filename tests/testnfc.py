#!/usr/bin/env python

import sys
sys.path.append("/home/osmc/Scripts/nfcpy/trunk/")
import nfc

print "Starting..."

clftty = nfc.ContactlessFrontend('tty')

# If everything is working, this should print: '   on /dev/ttyAMA0'
#print clftty

def on_connect(tag):
	#print "Tag has connected."
	print "Starting on_connect..."

	tagID = str(tag).split("ID=", 1)[1]
	# DEBUG - Check for kill tag
	if (str(tagID) == "046B435A002980"):
		# Reading this tag should kill the program cleanly.
		print "Kill tag read. Shutting script down..."
		closeReader()
		return

	print "Exiting on_connect."
	return True

def on_startup(targets):
	# Fires every single time clftty.connect is fired
	print "on_startup: fired"
	return

def on_release(tag):
	print "Tag has released."	
	return True

def closeReader():
	global clftty
	global loop 

	# Close the reader
	clftty.close()

	loop = False
	return

rdwr_options = {
	'on-connect': on_connect,
	'on-release': on_release,
	#'on-startup': on_startup,
}

loop = True
while loop == True:
	#print "Top of the loop"
	if (on_connect):
		print "on_connect = True"
	elif not (on_connect):
		print "on_connect = False"
	elif (on_release):
		print "on_release = True"
	else:
		print "Got to here"

	tag = clftty.connect(rdwr=rdwr_options)
	print "clftty.connect(): fired"
