#!/usr/bin/env python
#TODO# !/usr/bin/env python3
#
# modulator / demodulator for OrthoModulation
#
# This is a first stab at a radio modem that uses
# frequency hopping over 32 frequencies, transmitting
# the same signal on each, but with increasing delay.
# The channel identity identities the order and the
# orthogonality of randomisation turns other orders
# into mere produces of noise.
#
#TODO# Get working: Multiple same-time submissions
#TODO# Compute signal variance
#TODO# Can we polish/sharpen the FFT result in  input?
#TODO# Can we polish/soften  the FFT result on output?
#
# From: Rick van Rein (PA1RVR)


from math import floor
#TODO# Python3 has choices() too
from random import choice, uniform, shuffle

from numpy.fft import fft, ifft


# Construct a random receiver identity
#
receiver = [ x for x in range (32) ]
print ('Receiver = %r' % receiver)
shuffle (receiver)
print ('Shuffled receiver = %r' % receiver)

# Generate a digital signal sequence, random "0" and "1" data
#
testsz = 1024
dout = [ floor (uniform (0,65536)) for _ in range (testsz) ]
print ('Data out = %r' % dout [32:])

# Form frequency outputs and map to time outputs
#
fouts = [ [0] * 32 for i in range (testsz) ]
for fidx in range (31,testsz):
	for fofs in range (32):
		#DEBUG# print ('fidx = %d/%d, fofs = %d/%d, fidx-fofs = %d/%d' % (fidx,len(fouts),fofs,len(receiver),fidx-fofs,len(dout)) )
		fouts [fidx] [receiver [fofs]] = dout [fidx-fofs]
#DEBUG# print ('Fouts = %r' % fouts [32:])
touts = [ ifft (fout) for fout in fouts ]

# Send and receive... ahum, by copying output to input :)
#
# I know, I know, a real Radio Amateur has most fun here.
# If it wasn't for the eggs, I might even eat quiche...
#
tins = touts

# Map time-based inputs to frequency-based inputs
#
fins = [ fft (tin) for tin in tins ]
#DEBUG# print ('Fins = %r' % fins [32:])

# Retrieve the symbols following their independent sync sequences
#
din = [ 0 ] * testsz
for fidx in range (31,testsz):
	for fofs in range (32):
		#DEBUG# print ('fidx = %d/%d, fofs = %d/%d, fidx-fofs = %d/%d' % (fidx,len(fouts),fofs,len(receiver),fidx-fofs,len(dout)) )
		din [fidx-fofs] += fins [fidx] [receiver [fofs]] / 32.0
print ('Data in = %r' % din [32:])

# Derive if din and dout (from 31) are sufficiently close
#
for fidx in range (31,testsz-31):
	if abs (dout [fidx] - din [fidx]) >= 0.5:
		print ('Big difference at %d: %f != %f' % (fidx,dout[fidx],din[fidx]) )
