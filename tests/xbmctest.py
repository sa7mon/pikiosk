#!/usr/bin/env python

import requests
import json
import urllib

def executeRPC(rpcpayload):
	# Kodi config #
	kodi_host = 'localhost'
	kodi_port = 80
 
	#Base URL of the json RPC calls. For GET calls we append a "request" URI 
	#parameter. For POSTs, we add the payload as JSON the the HTTP request body
	kodi_json_rpc_url = "http://" + kodi_host + ":" + str(kodi_port) + "/jsonrpc"
	
	url_param = urllib.urlencode({'request': json.dumps(rpcpayload)}) 
	
	return requests.get(kodi_json_rpc_url + '?' + url_param,headers={'content-type': 'application/json'})

#Payload for the method to get the currently playing / paused video or audio
payload1 = {"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}
payload2 = {"jsonrpc": "2.0","id": "1", "method":"player.open", "params": {"item": {"file" : "/home/osmc/Movies/Sample1.mp4"}, "options": {"repeat": "all"}}}
payload3 = {"jsonrpc": "2.0", "id": "1", "method": "JSONRPC.Version"}
payload4 = {"jsonrpc": "2.0","id":	1,"method": "Playlist.Add","params": {"playlistid": 1,"item": {"file": "/home/osmc/Videos/Sample1.mp4"}}}
plClearPlaylist = {"jsonrpc": "2.0","id": 1,"method": "Playlist.Clear","params": {"playlistid": 1}}
payload5= {"jsonrpc": "2.0","id": 1,"method": "Playlist.Add","params": {"playlistid": 1,"item": {"file": "/home/osmc/Videos/Sample-Standby.mp4"}}}
payload6 = {"jsonrpc": "2.0","id": 1,"method": "Player.Open","params": {"item": {"playlistid": 1}}}
payload7 = {"jsonrpc": "2.0","id": 1,"method": "Playlist.GetItems","params": {"playlistid": 1}}
plPlayerRepeat = {"jsonrpc": "2.0","id": 1,"method": "Player.SetRepeat","params": {"playerid": 1,"repeat": "all"}}

print "Clearing playlist"
print executeRPC(plClearPlaylist).text

print "Adding first video to playlist"
print executeRPC(payload4).text

print "Opening player"
print executeRPC(payload6).text

print "Getting playlist info"
print executeRPC(payload7).text

print "Clearing playlist"
print executeRPC(plClearPlaylist).text

print "Adding standby video to playlist"
print executeRPC(payload5).text

print "Setting repeat to one"
print executeRPC(plPlayerRepeat).text
