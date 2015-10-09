#!/usr/bin/env python

# Reads a file into a dictionary
# File needs to be in key=value format

def read(file, mode):
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

myDict = read("videoscolors.txt", "lights")
print myDict
