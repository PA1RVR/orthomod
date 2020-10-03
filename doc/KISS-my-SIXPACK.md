# KISS and 6PACK

> *The communication of AX.25 with a Terminal Node Controller
> is usually over a TTY-based protocol like KISS or 6PACK.
> How are the responsibilities layered?*

For NRZI/BPSK, the layering of frame processing is:

  * Application provides a frame
  * AX.25 adds fields around the frame
  * TNC adds CRC and Flag Fields
  * TNC applies bit stuffing
  * TNC applies NRZI encoding
  * TNC transmits BPSK

For TPSK, the layering of frame processing would be different:

  * Applicatio provides a frame
  * AX.25 adds fields around the frame
  * TNC adds CRC and Flag Fields
  * TNC applies bit stuffing
  * TNC transmits TPSK

Note that the TNC, or a simulated TTY device on Linux,
serves for CRC and Flag Fields, bit stuffing and actual
transmission.  This indicates that we can do without the
NRZI encoding for TPSK, even if it is a very good idea
for BPSK.

For TPSK, we have a more elaborate distinction; not just
between "no change" and "transmit 0", but we also explictly
model "transmit 1" and thereby add a clock trigger to the
bit values, which is why we call them "clocked 0" and
"clocked 1".  Under such a modulation, NRZI would only be
in the way! and it does not have to be, not on Linux, not
if we program our own TNC-simulating TTY interface.

