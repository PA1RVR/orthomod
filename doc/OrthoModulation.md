# OrthoModulation: Design Rationale

> *The purpose of OrthoModulation is to allow multiple
> senders to transmit on the same bandwidth, and exploit
> the superposition principle that applies to AM to
> still get all the signals to go through.*


**Superposition** is a property of linear systems; if you
have an effect that applies to two simultaneous runs, then
it also applies to all linear compisitions (meaning, weighted
additions) of the independent runs.

So, even when two transmitters broadcast at the same time,
their signals merely get added.  In terms of AM, this means
their volumes get added.  (In comparison, FM/PM transmissions
get competitive and every receiver would elect a winner, or
toggle between momentary winners.)

The addition will not yield the same results in all places,
as a result of varying delay times and frequencies bouncing.
This is not a problem because the same principles still
apply.

**Fourier Transform** is used in many radio codecs to transmit
at multiple frequencies simultaneously, and rely on a spread
of information over the so-acquired spectrum of orthogonal
(or independent) frequencies.  The transformation itself
maps between this frequency-based information and a
time-based signal that can be transmitted over radio waves.

Fourier transformation is a linear process, itself founded
on the superposition of individual waves.

**Echo cancellation** is a well-known technique in audio
circuits, where any bounces of the locally generated
signal are removed.  This is particularly useful whenever 
a signal can bounce back with a delay.  It works by sampling
the responses of transmissions and seeking the consistent
pattern of receiving it back at later times.  Since all the
other reception appears random in comparison to the locally
tranmsitted signal, the other stations tend to cancel out
in a slow-enough learning process.  This can be used to
allow a radio to receive on the same set of frequencies
over which it also transmits.  The activity can be
performed once on the time-based signal, instead of on each
individual frequency.

Under echo cancellation, a radio transmitting to itself
would not receive the signal.  In cases where it is desired
to address oneself, a local loopback must be used instead.

Echo cancellation is a linear process.

**Amplitude Modulation** is a linear modulation technique,
in that the amplitudes from multiple transmission stations
can be added.  Each receveiver will get its own view on the
composed signal, as a result of the delays and paths between
each transmitter and receiver.  However, with bounces of a
radio's own transmissions removed through echo cancellation,
some addition of signals will arrive.  This helps us to
understand that timing and volume cannot be driven as desired,
and so, that attempts to synchronise transmitters is probably
not useful.

Proper handling of simultaneous transmissions is possible
with AM, not FM or PM.  It is however possible to transmit
multiple frequencies in a small bandwidth, and treat each
separately.  To process the composed signal as well as
possible, it should be treated as fullblown AM and passed
through the Fourier Transform for later processing; early
detection of OOK, BPSK or QAM would interfere with the
superposition in the receiver.

The trick is now to find a suitable encodig for values "0"
and "1".  The customary encodings are:

  * **OOK** would transmit "0" as silence and "1" as a
    signal.  One might say that "1" has absolute
    priority over "0" except for rare situations of
    cancellation of exactly opposing transmissions.
    The phase and amplitude would normally change, but
    it is easy to detect the "1" transmitted.  The
    problem here is that as more transmitters are added
    it becomes increasingly difficult to ever send "0"
    signals.

  * **BPSK** transmits opposing phases for "0" and "1",
    and as a result these values may cancel out one
    another.  This cancellation is useful inasfar as
    random values are being added with the purpose that
    they cancel each other out.  This could also
    accommodate for differentiations in phase and path
    timing, especially with many active transmitters.
    Chances of cancellation also improve as more random
    bits are combined.

  * **QPSK and QAM** place more points in the constellation
    diagram.  This raises difficulty in detection when
    various transmitters arrive at different strengths and
    different delays; the constant scale expected by the
    constellation diagram would not be available after
    adding signals.  This is not going to be useful.

  * **TPSK** or Triple Phase Shift Keying is a design
    alternative that would continue with the same signal
    if nothing changes, move the phase forward for a "1"
    and backward for a "0".  The three phases are equally
    distributed over a circle.

The BPSK form is perhaps the most interesting choice, also
because it is usually possible to distinguish the phase of "1"
and "0" signals, the absense of a signal and the presumably
common imperfect cancellation which leads to unexpected phases.

Interesting about BPSK is that each transmitter changes phase
at regular time intervals, in a clearly opposite direction,
and that others often change at different times and in
different directions.  This helps to focus on one transmitter
in a sea of many.  Even when this is imperfect, it can be
part of a selection process than spans more frequencies.

**NRZI** enables the interpretation of BPSK when its phase
at the transmitter is unknown, as is the case when transmitters
can be added at will.  The transmission of a logical "0" is
translated to a phase change and a logical "1" is no change.
In this case, a "0" always wins, but its angle is of importance
and may help to identify the transmitter, at least in part.
NRZI should not be used when modulating with TPSK.

**Bit Stuffing** is the practice of inserting a bit to break
a special pattern.  In HDLC, sequences of more than one
consecutive "1" bit are special; the sequence "01111110" is
a frame synchronisation signal and more than six consecutive
"1" represent a frame break.  This signaling function is useful
in all HDLC variants.  An added value for NRZI is the certainty
of a regular phase change to feed a PLL, which is useful for
single-transmitter BPSK systems; it is less useful for OrthoMod
but is nonetheless necessary, even for TPSK transmission.

**Clock Derivation** is possible when a mechanism such as
HDLC over NRZI is used.  One example of this would be AX.25
over NRZI over BPSK.  Regular "0" bits are transmitted, and
translated to regular phase changes.  Only to break off a
transmission would there ever be more than 6 signals "1" on
the air.  During the several-bit-long "1" periods, the signal
does not change and the clock is interpolated.  This is possible
due to the synchronous nature of the serial PHY; it does not
need an explicit clock signal.  Note that this renders variable
transmission speeds impossible.  An alternative option is to
send a bit clock over asynchronous radio, based on TPSK and no
intermediate NRZI layer.  It is now actually possible
to slow down transmission, perhaps even support irregular
bit speeds, to accommodate noise traversal.  Only frequency
hopping for reasons of redundancy is part of the complete
radio discipline and must take place at a fixed pace.

**Clocking Bits** can be transmitted with TPSK, because it
separates stable, "1" and "0" values.  Specifically, the stable
state is not interpreted as a new value because the actual bit
values are active changes.  Neither "1" nor "0" wins over the
other, and the (almost) simultaneous occurrence of both
leads to a new signal that might be interpreted in a sensitive
receiver, namely a sign reversal with a possible glitch when
they do not arrive at the exact same point.  Importantly
though, there is no cancellation and so no loss of information.
Vector addition makes sense in this scheme, but the amplitude
is not interpreted and so the confusion of QAM can be avoided.

**Coded Spreading** interleaves a signal with a code to
spread it over an available bandwidth.  It does not assign
explicit frequencies, and is not generally processed via
Fourier Transformation.  When hopping between frequencies,
the ideas for coded and frequency division multiplexing
come together, and the linearity of Fourier Transformation
can be exploited.

We imagine a transmitter to jump between frequencies in
a personalised pattern, causing changes to the signal
transmitted over each as needed.  For instance, when
using NRZI transmission, the transmission of a "0" bit
causes a change and the transmission of a "1" bit does
not.

**Redundancy** in transmitted bits helps to improve the
certainty of a signal being received.  This is important
when all the other transmitters count as random noise
added to the locally generated signal; although these
random others cancel each other on average, it does not
necessarily occur for any single bit.  Redundancy then
helps to collect more evidence that we are consistently
transmitting a "1" or a "0" bit.

**Identity** is a number that every receiver allocates
at random, or otherwise derived from a radio amateur's
call sign in posession of the receiving station.  The
seemingly random nature of these numbers means that
they effectively cancel out, on average.  Identity is
used to derive (with div/mod sequences) the various
frequencies over which a station transmits.  These
frequencies can be addressed in a sequence to transmit
a bit redundantly, and receivers can decode by following
their own frequency hopping order, find the BPSK pattern
of redundant change and direction to recognise the
transmitter that consistently sends to the receiver's
identity.

**Channels** should be allocated, with fresh identity to
use the same set of frequencies in another hopping order,
to separate point-to-point connections that should be
used without continued clashes as could occur when more
than one transmitter sends to the same receiver at
precisely the same time.  The channel would still be
used to ask a receiver to open a new channel.  Since
we are assuming echo cancellation, a channel can be
bidirectional.

**Simultaneous Reception** is possible as long as two
transmitters do not send at the exact same timing to
the exact same channel.  Once a first transmitter has
sent a bit to a frequency, it hops to the next and
the first frequency is freed, listening for another
transmitter.  When a clash occurs, the receiver may
send an alert signal to itseld, and hope the clashed
transmitters would detect; it could also be left to
a higher layer protocol to miss an acknowledgement
and resend after a random interval.

The expense of simultaneous reception is as low as
a series of additions per identity/channel received.
Specifically, the same FFT can be shared.

**Simultaneous Transmission** is possible as long as
it is done to different receiving channels, or as
long as the signals are at least one bit position
apart.  One simply triggers that verious bits in the
output.  Assuming that all such transmissions occur
in lockstep as dictated by the sample period of the
Fourier Transformation, signals targeted at different
receivers might coincide on the same frequency for
the duration of one bit transmission.  In that case,
two times "1" is simply "1" and two times "0" is
simply "0", but combinations of "1" and "0" should be
transmitted as no signal.  Both values would then pull
back to zero in the direction of the expected change,
but get halfway the normal amplitude.  Half a hint
is better than no hint, or a wrong hint, especially
under redudant transmission

The expense of simultaneous transmission is as low as
a series of additions per identity/channel transmitted.
Specifically, the same FFT can be shared.

**AX.25** is a form of HDLC, filling in details such as
addressing for the use by radio amateurs.  It is not the
only possible protocol, certainly not for a synchronous
serial connection based on TPSK.  The property of AX.25
should regularly transmit the identifier of the radio
amateur is however assured.  In fact, it is redundantly
assured over all the frequencies used.  The one legal
concern remaining is whether TPSK is a legally acceptable
form of doing this.  This may be part of the choice between
NRZI/BPSK and TPSK variants for the transmission.

**MAC/PHY Linkage** is mostly concerned with finding
PHY addresses for given packet addressing at the MAC
layer.  AX.25 addresses are radio amateur call signs,
and the PHY routes them from one call sign to another,
even when proxying there will be such a pair.  As a
general idea, the channel identity may be the hash of
such a pair (leading to a different channel for send
and receive, making echo cancellation less important).
Only when connecting, or when sending frames outside
a connection, should only the target address be used;
this allows a receiver to listen to their own address
and welcome attempts to open new connections.  This
falls within the sphere of the AX.25 layer.

