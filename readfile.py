#!/usr/bin/env python

# Reads a file into a dictionary
# File needs to be in key=value format

def read(file, mode):
	if not ((mode == "videos") or (mode == "lights")):
		print "bad mode, friend"

	readDict = {}
	with open(file, "r") as text:
		for line in text:
			# For each line in the test file, do the following
            		# Split the line into 2 lines delimited by the equal sign
            		# Make the first string the dict key and the second the dict value
			readDict[line.split('=', 2)[0]] = line.split('=', 2)[1].strip('\n')
		# print readDict
	return readDict 

myDict = read("videos.txt", "lights")
print myDict
