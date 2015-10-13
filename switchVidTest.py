#!/usr/bin/env python

import time
import subprocess
from pyomxplayer import OMXPlayer

# Takes about 4 seconds for the video to actually start playing
omx1 = OMXPlayer('/home/pi/Videos/Sample1.mp4')
print "Playing video 1"

time.sleep(9)

omx2 = OMXPlayer('/home/pi/Videos/Sample1.mp4')
print "Starting video 2"
time.sleep(3.69) # Somewhere between 3 and 3.75 seconds. Whatever the time is between the call to OMXPlayer and when it actually plays
print "Time is up"

omx1.stop()
print "Stopping video 1"


# Play video 
#call(["omxplayer", "/home/pi/Videos/Sample1.mp4"], close_fds=True, stderr=None, stdout=None)

'''
pid1 = subprocess.Popen(["omxplayer","/home/pi/Videos/Sample1.mp4"]).pid
print pid1
# Wait 5 seconds

time.sleep(5)
pid0 = subprocess.Popen(["kill", pid1]).pid
# Play video again and see how it switches
pid2 = subprocess.Popen(["omxplayer","/home/pi/Videos/Sample1.mp4"]).pid
print pid2
'''

