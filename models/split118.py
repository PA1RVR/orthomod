#!/usr/bin/env python3
#
# Figure out how numbers 32..2 can be split into 16-bit integers.
#
# This was input to the identity derivation scheme, see
# doc/ChannelIdentity.md
#
# We ended up using half the SHA256 output size, or 8 values
# of 16 bit each.  The div-mod for 3,2 are moved to another
# word to get that working (and must be remembered until it
# is their turn).
#
# From: Rick van Rein (PA1RVR) <rick@openfortress.nl>


max=[]
do=[]

sofar=1
doing=[]
for i in range (32,1,-1):
	if sofar*i >= 2**16:
		max.append (sofar)
		do.append (doing)
		sofar = 1
		doing = []
	sofar *= i
	doing.append (i)
if doing != []:
	max.append (sofar)
	do.append (doing)

print (do)
print (max)

