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
import nfc, requests, json, urllib, time
from neopixel import *

################# VARIABLES #######################

# Our flag to keep looping later
loop = 1

# The text file containing our video names, tagIDs, and light colors
fileVideos = "videos.txt"

# The folder containing all the videos to play
dirVideos = "/home/osmc/Videos/"

# File to loop while waiting for tag
fileStandbyVideo = "Sample-Standby.mp4"

# Kodi config #
kodi_host = 'localhost'
kodi_port = 80

# JSON-RPC payloads to send to Kodi on localhost
plPlaylistClear = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "Playlist.Clear",
    "params": {"playlistid": 1}
}
plPlaylistAddStandby = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "Playlist.Add",
    "params": {
        "playlistid": 1,
        "item": {"file": dirVideos + fileStandbyVideo}
    }
}
plPlayerOpen = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "Player.Open",
    "params": {"item": {"playlistid": 1}}
}
plPlayerSetRepeat = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "Player.SetRepeat",
    "params": {"playerid": 1, "repeat": "all"}
}
plPlayerStop = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "Player.Stop",
    "params": {"playerid": 1}
}

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


###############   FUNCTIONS  #################

def closeReader():
    """ Close the reader and stop watching for tags. """
    global loop

    # Turn the LED ring off
    solidColor(strip,0,0,0,0)

    # Close the reader
    clf.close()

    # Then set loop to not 1 to cleanly exit program instead of suspending it.
    loop = 0
    return

def executeRPC(rpcpayload):
    """ Execute the payload on the Kodi server JSON-RPC API. """

    #Base URL of the json RPC calls. For GET calls we append a "request" URI
    #parameter. For POSTs, we add the payload as JSON the the HTTP request body
    kodi_json_rpc_url = "http://" + kodi_host + ":" + str(kodi_port) + "/jsonrpc"

    url_param = urllib.urlencode({'request': json.dumps(rpcpayload)})

    # Return the server's response to our request.
    # If not a get method, will return status of request (hopefully 200)
    return requests.get(kodi_json_rpc_url + '?' + url_param, headers={'content-type': 'application/json'})

def on_connect(tag):
    """
    When a tag is read, play that video

    Function is fired when a tag is present, and only returns
    once the tag is released. Look up the tagID in the
    dict of videos to find the video play, then execute
    that RPC payload. Then queue up the standby video and
    loop it.

    Arguments:
    tag - type: nfc.tag.Tag
        (http://nfcpy.org/latest/modules/tag.html#nfc.tag.Tag)

    Returns:
    true - Only return true when the tag is released.

    """

    # Get the tag's ID
    tagID = str(tag).split("ID=", 1)[1]

    # DEBUG - Check for kill tag
    if str(tagID) == "046B435A002980":
        # Reading this tag should kill the program cleanly.
        print "Kill tag read. Shutting script down..."
        print executeRPC(plPlayerStop).text
        closeReader()
        return

    # Check if the tag exists in both dictionaries
    if not ((tagID in videoDict) and (tagID in lightsColorsDict)):
        print "This tag doesn't exist in one of the dictionaries."
        return True
    else:
        #Get video filename to play: e.g. Sample1.mp4
        video = videoDict.get(tagID)

        #Get color to change ring to 
        color = lightsColorsDict.get(tagID)

        # Change ring to appropriate color
        #solidColor(strip, 150, int(color.split(",", 3)[0]),int(color.split(",", 3)[1]),int(color.split(",", 3)[2]))

        colorWipe(strip, 250, Color(int(color.split(",", 3)[0]),int(color.split(",", 3)[1]),int(color.split(",", 3)[2]) ), 5)

        # Clear playlist
        print "Clearing playlist"
        print executeRPC(plPlaylistClear)

        # Add the appropriate video the playlist
        print "Adding specific video to playlist"
        plAddVideo = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "Playlist.Add",
            "params": {
                "playlistid": 1,
                "item": {"file": dirVideos + video}
            }
        }
        print executeRPC(plAddVideo).text

        # Switch to next item in playlist (the video we just added)
        print "Switching to next video in the playlist"
        plNextVideo = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "Player.goto",
            "params": {
                "playerid": 1,
                "to": "next"
            }
        }
        print executeRPC(plNextVideo).text

        # Clear playlist
        print "Clearing playlist"
        print executeRPC(plPlaylistClear)

        # Add standby video to playlist
        print "Adding standby video to playlist"
        print executeRPC(plPlaylistAddStandby)

        # Set player repeat to 'one'
        print "Setting player repeat to one"
        print executeRPC(plPlayerSetRepeat)



        return True

def readFile(filename, mode):
    """
    Read a specially-formatted text file into a dict

    Reads a text file at location 'filename' into a
    returned dict. Since our text file has 3 columns,
    readFile() will have to be run twice. Once for each
    dict to create.

    Arguments:
    filename - type: String - Can be relative or absolute,
        needs to be formatted in format: tagID=file=lightcolor
    mode - type: String - Allowed: "videos", "lights"

    Returns:
    readDict - type: dict - Will return empty if 'mode' is not
        an allowed value.
    """
    # file data needs to be in 'key=video=color' format
    # mode can be either "videos" or "lights"

    # Initialize a blank dictionary to fill and then return
    readDict = {}

    # Check to make sure the mode passed is one of the approved 2
    if not ((mode == "videos") or (mode == "lights")):
        print "Error: read(): Bad mode passed"
        return readDict

    # Open the file as text
    with open(filename, "r") as text:
        # For each line in the test file, do the following
        # Split the line into 2 lines delimited by the equal sign
        # Make the first string the dict key and the second the dict value
        for line in text:
            if mode == "videos":
                readDict[line.split('=', 2)[0]] = line.split('=', 2)[1].strip('\n')
            elif mode == "lights":
                readDict[line.split('=', 3)[0]] = line.split('=', 3)[2].strip('\n')
    return readDict

def solidColor(strip, brightness, R, G, B):
    # Changes the whole ring to one solid color.
    # To "blank out" the ring, call any color and set brightness to 0
    for i in range(strip.numPixels()):
        strip.setPixelColorRGB(i,R,G,B)
    strip.setBrightness(brightness)
    strip.show()

def whitePulse(strip, ceiling, wait_ms=20):
    while something: 
        for j in range(ceiling): 
            for i in range(strip.numPixels()):
                strip.setPixelColorRGB(i, 127, 127, 127)
            strip.show()
            time.sleep(wait_ms/1000.0)
            # Change the strips brightness
            strip.setBrightness(j)
            # Once we get to the top of the brightness, start fading down instead of up
            if j == (ceiling - 1):
                print "Hit the top!"
                for j in range((ceiling - 2), 0, -1):
                    for i in range(strip.numPixels()):
                        strip.setPixelColorRGB(i, 127, 127, 127)
                    strip.show()
                    time.sleep(wait_ms/1000.0)
                    # Change the strips brightness
                    strip.setBrightness(j)

def colorWipe(strip, brightness,color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.setBrightness(brightness)
        strip.show()
        time.sleep(wait_ms/1000.0)


##################   MAIN PROGRAM   #######################

# Read the file with videos and tag IDs into a dict
print "Reading videos file..."
videoDict = readFile(fileVideos, "videos")
lightsColorsDict = readFile(fileVideos, "lights")

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

solidColor(strip,50,127,127,127) #Dim white

# Setup our reader connection through UART
# To diagnose issues:
#   To verify from Python CLI, print(clf) should result in /dev/AMA0
#   Alternately, 'tty:AMA0:pn532' will probably work in place of 'tty'
print "Initiating reader..."
try:
    clf = nfc.ContactlessFrontend('tty')
except IOError:
    print "Couldn't initialize reader (IOError)"
else:
    # Clear playlist
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
    # Make loop not 1 to stop waiting for tags.
    while loop == 1:
        print "Waiting for tag to read..."
        clf.connect(rdwr={'on-connect': on_connect})
        solidColor(strip,50,127,127,127) #Dim white
