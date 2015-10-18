#!/usr/bin/env python

import sys
sys.path.append("/home/osmc/Scripts/nfcpy/trunk/")
import nfc

clftty = nfc.ContactlessFrontend('tty:AMA0:pn532')

# If everything is working, this should print: '   on /dev/ttyAMA0'
print clftty
