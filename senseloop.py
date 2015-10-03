#!/usr/bin/env python
#
# Written by: Dan Salmon
# Created on: 10/02/15 
#
import nfc 

def connected(tag):
    print(tag);
    return

print "Initiating reader...";
clf = nfc.ContactlessFrontend('tty');

print "Waiting for tag to read...";
clf.connect(rdwr={'on-connect': connected});
