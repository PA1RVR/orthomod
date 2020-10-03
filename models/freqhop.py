#!/usr/bin/env python3
#
# Frequency Hopping Plan for radio amateur call signs with station id.
#
# From: Rick van Rein (PA1RVR) <rick@openfortress.nl>


import sys
from math import trunc
from hashlib import sha256

if len (sys.argv) != 3:
	sys.stderr.write ('Usage: %s xmit recv\nWhere the parameters are a radio amateur call sign with station id\nExample: %s PA1RVR-3 PA1RVR-12' % (sys.argv [0],sys.argv [0]))
	sys.exit (1)

xmit = sys.argv [1].upper ()
recv = sys.argv [2].upper ()

xmitbincode = sha256 (xmit.encode ('utf-8')).digest ()
recvbincode = sha256 (recv.encode ('utf-8')).digest ()

xmithexcode = sha256 (xmit.encode ('utf-8')).hexdigest ()
recvhexcode = sha256 (recv.encode ('utf-8')).hexdigest ()

xmitrotbincode = xmitbincode [16:] + xmitbincode [:16]
recvrotbincode = recvbincode [16:] + recvbincode [:16]

xmitrothexcode = xmithexcode [32:] + xmithexcode [:32]
recvrothexcode = recvhexcode [32:] + recvhexcode [:32]

print ('Xmit %s = %s' % (xmit,xmithexcode))
print ('Recv %s = %s' % (recv,recvhexcode))
print ('Xrot %s = %s' % (xmit,xmitrothexcode))
print ('Xrot %s = %s' % (recv,recvrothexcode))

chanhexcode = ''.join ([ '%02x' % (xmitrotbincode [i] ^ recvbincode [i]) for i in range (16) ])
crevhexcode = ''.join ([ '%02x' % (recvrotbincode [i] ^ xmitbincode [i]) for i in range (16) ])

print ('Chan %s->%s = %s' % (xmit,recv,chanhexcode))
print ('Chan %s->%s = %s' % (recv,xmit,crevhexcode))

hexid_divors = { }
hexid_divors [ 0] = [32, 31, 29, 28, 27, 6, 5]
hexid_divors [ 8] = [26, 25, 24, 23, 22, 21, 4]
hexid_divors [16] = [20, 19, 18, 17, 16, 15, 14, 2]
hexid_divors [24] = [30, 13, 12, 11, 10, 9, 8, 7, 3]
#
def hexid2freqhop (hexid):
	work = 0
	choix = { 1: 0 }
	for pos0 in range (0,32,8):
		work = int (hexid [pos0:pos0+8], 16)
		for divor in hexid_divors [pos0]:
			choix [divor] = work % divor
			work = trunc (work / divor)
	values = [ '%d' % i for i in range (32) ]
	retval = [ ]
	while len (values) > 0:
		cx = choix [ len (values) ]
		retval.append (values [cx])
		del values [cx]
	return ','.join (retval)

chanfreqhop = hexid2freqhop (chanhexcode)
crevfreqhop = hexid2freqhop (crevhexcode)

print ('Freq %s->%s = %s' % (xmit,recv,chanfreqhop))
print ('Freq %s->%s = %s' % (recv,xmit,crevfreqhop))
