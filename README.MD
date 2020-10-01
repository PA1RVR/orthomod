# OrthoModulation and TPSK

> *This repository provides descriptions, models and code for an
> orthogonal radio modulation technique; multiple senders and
> multiple receivers can work on the same frequency band at the
> same time.  TPSK turns the radio channel into a synchronous serial
> device.*

The design that is growing here allows multiple radios to
transmit at the same time, on the same bandwidth.  This can
be analysed on receiving radios.  In general, simultaneous
connections between transmitters and receivers are possible.
Nothing stops a single transmitter from addressing more than
one receiver at the same time, and nothing stops areceiver
from accepting more than one transmitter at the same time.

The bandwidth is split into frequencies, each of which carry
the modulated signal with a different time delay.  The order
in which the delay is assigned to the various frequencies is
a code that determines who is the targeted recipient for the
signal.  Receivers look for coherent patterns between the
received traffic and their delays over the various frequencies.

It is possible for a receiver to process signals addressed
at multiple identities; in fact, this is a relatively cheap
form of processing.  Likewise, transmitters can pass signals
to multiple receiving identities.

We refer to the traffic to a given identity as a channel;
usually, a channel is identified by either a receiver alone
(for unconnected including connecting traffic) or by the
couple of transmitter and receiver (for connected traffic).
The transmitter or receiver may be a proxy station; this
means that its incoming and outgoing channel bear different
identities.  When groups want to share an identity, they
can create one with any reasonable mechanism that leads
to sufficiently scattered identities with a minimum risk
of identity clashes.

At the level of radio waves, orthogonal addition is not
optimal with existing modulation techniques such as BPSK,
QPSK or QAM, even if the underlying AM encoding technique
is suited.  We introduce a new modulation technique called
TPSK, which distinguishes three kinds of signaling, namely
"no change", "clocked 0" and "clocked 1".  The last two can
be actively measured.  When both occur at the same time
due to independent transmissions than this can be detected
and treated as a lower probability of having found a match.
Using long enough codes, this should not cause problems as
long as a channel is used by only one transmitter at a time.

**Read more:**

  * [Design Documentation](doc/OrthoModulation.md)
  * [Thoughts about AX.25 integration](doc/AX25.md)
  * [Identity and Per-Frequency Delays](doc/identity.pdf)
  * [Constellation Diagram for TPSK](doc/tpsk.png)
  * [Block Diagram with AX.25 / NRZI / BPSK](doc/orthomod-bpsk.pdf)
  * [Block Diagram with AX.25 / TPSK](doc/orthomod-tpsk.pdf)

This work is done by PA1RVR from the Netherlands, a member of
[Experimental Telecoms Group Drienerlo](https://etgd.utwente.nl/english/)
located at the
[University of Twente](https://www.utwente.nl/).

