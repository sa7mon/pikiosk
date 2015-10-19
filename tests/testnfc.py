#!/usr/bin/env python

import sys
sys.path.append("/home/osmc/Scripts/nfcpy/trunk/")
import nfc

print "Starting..."

clftty = nfc.ContactlessFrontend('tty:AMA0:pn532')

# If everything is working, this should print: '   on /dev/ttyAMA0'
#print clftty

def on_connect(tag):
	print "on_connect: fired"
	print(tag)

def on_startup(targets):
	# Fires every single time clftty.connect is fired
	print "on_startup: fired"

	#loopme = True
	#while loopme == True:
		# Do something
	#	print " "
	
	
	return

rdwr_options = {
	'on-connect': on_connect,
}

loop = True
while loop == True:
	print "Top of the loop"
	tag = clftty.connect(rdwr=rdwr_options)

#tag = clftty.connect(rdwr=rdwr_options)
