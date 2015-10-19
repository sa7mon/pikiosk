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
import requests
import json
import urllib

###############   FUNCTIONS  #################

def closeReader():
	global clf
	global loop 

	# Close the reader
	clf.close()

	# Then set loop to not 1 to cleanly exit program instead of suspending it.
	loop = 0
	return

def executeRPC(rpcpayload):
	# Kodi config #
	kodi_host = 'localhost'
	kodi_port = 80
 
	#Base URL of the json RPC calls. For GET calls we append a "request" URI 
	#parameter. For POSTs, we add the payload as JSON the the HTTP request body
	kodi_json_rpc_url = "http://" + kodi_host + ":" + str(kodi_port) + "/jsonrpc"
	
	url_param = urllib.urlencode({'request': json.dumps(rpcpayload)}) 
	
	return requests.get(kodi_json_rpc_url + '?' + url_param,headers={'content-type': 'application/json'})

def on_connect(tag):
	global videoDict
	global lightsColorsDict
	
	# Get the tag's ID 
	tagID = str(tag).split("ID=", 1)[1]

	# Check if the tag exists in both dictionaries
	if not ((tagID in videoDict) and (tagID in lightsColorsDict)):
		print "This tag doesn't exist in one of the dictionaries."
		return
	else: 
		#Get video filename to play: e.g. Sample1.mp4
		video = videoDict.get(tagID)
		print "video: " + video
		# Clear playlist
		print "Clearing playlist"
		print executeRPC(plPlaylistClear)
		# Add the appropriate video the playlist
		print "Adding specific video to playlist" #DEBUG HARDCODING VIDEO1 FOR NOW NEED TO CHANGE
		print executeRPC(plPlaylistAdd)
		# Open player
		print "Opening player..."
		print executeRPC(plPlayerOpen)
		# Clear playlist
		print "Clearing playlist"
		print executeRPC(plPlaylistClear)
		# Add standby video to playlist
		print "Adding standby video to playlist"
		print executeRPC(plPlaylistAddStandby)
		# Set player repeat to 'one'
		print "Setting player repeat to one"
		print executeRPC(plPlayerSetRepeat)

		
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

# File to loop while waiting for tag
fileStandbyVideo = "Sample-Standby.mp4"

# JSON-RPC payloads to send to Kodi on localhost
plPlaylistAdd = {"jsonrpc": "2.0","id":	1,"method": "Playlist.Add","params": {"playlistid": 1,"item": {"file": "/home/osmc/Movies/Sample1.mp4"}}}
plPlaylistClear = {"jsonrpc": "2.0","id": 1,"method": "Playlist.Clear","params": {"playlistid": 1}}
plPlaylistAddStandby = {"jsonrpc": "2.0","id": 1,"method": "Playlist.Add","params": {"playlistid": 1,"item": {"file": "/home/osmc/Videos/Sample-Standby.mp4"}}}
plPlayerOpen = {"jsonrpc": "2.0","id": 1,"method": "Player.Open","params": {"item": {"playlistid": 1}}}
plPlayerSetRepeat = {"jsonrpc": "2.0","id": 1,"method": "Player.SetRepeat","params": {"playerid": 1,"repeat": "all"}}


##################   MAIN PROGRAM   ####################### 

# Read the file with videos and tag IDs into a dict
print "Reading videos file..."
videoDict = readFile(fileVideos, "videos")
lightsColorsDict = readFile(fileVideos, "lights")


# Setup our reader connection through UART
# To diagnose issues:
# 	To verify from Python CLI, print(clf) should result in /dev/AMA0
# 	Alternately, 'tty:AMA0:pn532' will probably work in place of 'tty'
print "Initiating reader..."
try:
	clf = nfc.ContactlessFrontend('tty')
except IOError:
	print "Couldn't initialize reader (IOError)"
else: 
	# Start playing standby video
	print "Clearing playlist"
	print executeRPC(plPlaylistClear).text
	# Add standby video to playlist
	print "Adding standby video to playlist"
	print executeRPC(plPlaylistAddStandby).text
	# Set player repeat to 'one'
	print "Setting player repeat to one"
	print executeRPC(plPlayerSetRepeat).text
	# Open player
	print "Opening player"
	print executeRPC(plPlayerOpen).text
	
	# Continuously listen for tags nearby. Fire an event when we see one.
	# Make loop not 1 if loop needs to break
	while loop == 1: 
		print "Waiting for tag to read..."
		clf.connect(rdwr={'on-connect': on_connect})
	closeReader()
