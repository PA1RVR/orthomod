#!/usr/bin/env python3
#
# Figure out how numbers 32..2 can be split into 32-bit integers.
#
# This was input to the identity derivation scheme, see
# doc/ChannelIdentity.md
#
# We ended up using half the SHA256 output size, or 4 values
# of 32 bit each.
#
# From: Rick van Rein (PA1RVR) <rick@openfortress.nl>


from math import log


max=[]
do=[]

sofar=1
doing=[]
for i in range (32,6,-1):
	if i == 30:
		# 30 is manually distributed to initiate the 3rd list
		continue
	if i <= 6:
		# 2..6 are manually distributed over the lists
		continue
	if sofar*i >= 2**32/2 or i in [26]:
		max.append (sofar)
		do.append (doing)
		if len (do) < 3:
			sofar = 1
			doing = []
		else:
			sofar = 30
			doing = [30]
	sofar *= i
	doing.append (i)
if doing != []:
	max.append (sofar)
	do.append (doing)
# Manually divide
max [0] *= 6
max [0] *= 5
max [1] *= 4
max [2] *= 2
max [3] *= 3
do [0].append (6)
do [0].append (5)
do [1].append (4)
do [2].append (2)
do [3].append (3)

print (do)
print (max)
print ([log(m,2) for m in max])

