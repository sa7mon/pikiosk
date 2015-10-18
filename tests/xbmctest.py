#!/usr/bin/env python
import requests
import json
import urllib

def executeRPC(rpcdata):
	headers = {'content-type': 'application/json'}
	# Kodi config #
	kodi_host = 'localhost'
	kodi_port = 80
 
	#Base URL of the json RPC calls. For GET calls we append a "request" URI 
	#parameter. For POSTs, we add the payload as JSON the the HTTP request body
	kodi_json_rpc_url = "http://" + kodi_host + ":" + str(kodi_port) + "/jsonrpc"
	
	url_param = urllib.urlencode({'request': json.dumps(rpcdata)}) 
	
	return requests.get(kodi_json_rpc_url + '?' + url_param,headers=headers)



#Payload for the method to get the currently playing / paused video or audio
payload1 = {"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}
payload2 = {"jsonrpc": "2.0","id": "1", "method":"player.open", "params": {"item": {"file" : "/home/osmc/Movies/Sample1.mp4"}, "options": {"repeat": "all"}}}
payload3 = {"jsonrpc": "2.0", "id": "1", "method": "JSONRPC.Version"}


print "Response:"
print executeRPC(payload2).text
