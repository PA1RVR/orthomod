# Channel Identity for OrthoMod

> *Channels need an identity.  How to get to one?  And how does
> it translate to the frequency hopping model?*

We distribute the same signal over frequencies in a time-based
order, and use the order to derive an identity.  Receivers are
aware of the identities to match, and may support multiple at
rather low cost, after the FFT has come through.

The picture to keep in mind, simplified to 4 frequencies:

![Identity encoded as Frequency Hopping Order](identity.png)

The first identity is one from 4, the second chooses from the
remaining 3 and so on.  The number of possible identities is
therefore 4!=4x3x2x1=24.


## Many Identities

We can assign a default identity to every receiver, and use
that to reach it.  However, when multiple attempts to transmit
to the same receiver are sent, the risk of a clash is higher.
So, we try to have more channels at the (slight) expense of
analysing them separately after the FFT stage.

Channels may have different identities in both directions.
This introduce no cost for decoding, because the transmitter
and receiver are different processes anyway.  To increase the
likelyhood of spreading transmissions and perhaps allowing us
to drop echo cancellation in some cases, we prefer different
identities for different directions.

Groups may have their own idea of an identity.  We suggest
the use of a URI as a text.  It is impossible in general to
dictate a URI to be in canonical form, so this is up to the
user.  Note how `#xxx` fragments may always be added for local
processing, and how this might add a "secret" to encrypt the
group address.  **TODO:** *We may not have a way of relaying
the URI form to the radio layer, so is this prudent?*  Note
that several chat and broadcast applications are built on
top of AX.25 `UI` frames, using a fixed destination address.
For example, APRS defines prefixes that can be extended up to
6 characters and always the `-0` station.  These are pretty
much fixed destination addresses (note that radio amateurs
transmitting on radio amateur bands are required in many
legislations to regularly include the transmitter identity,
but not necessarily the receiver).

## Entropy for Identities

Entropy is the "amount of surprise" that an identity contains.
It helps us to spread identities; the more bits of entropy, the
more opportunity of distinguishing a signal from noise at the
same frequencies (including orthogonal transmissions).

It is commonly accepted that 128 bits of entropy leads to a
globally unique identity.  This assumes that no deliberate
attempts to clashes are made, of course, but other than that
a size of 128 bits is considered unique.

In AX.25 we can derive some entropy from the source and destination
addresses for a radio transmission.  Each address in AX.25 is coded
into 7 bytes, each holding 7 bits of data, so 49 bits each.  The
variants that can be derived are receiver-only (2^49 variants)
and transmitter-plus-receiver (2^98 variants) so we have a
total entropy of little over 98 bits, and that is overlooking
that not all syntaxes are permitted in the address fields.  There
may however be out-of-band identities communicated?
**TODO:** *We would then need to tie those to the radio layer,
somehow.  Not sure if that would work.  If not, we can send less
redundant signals, namely up to the permissable address forms,
which is well below 98 bits.*

The risk of a clash is not 2^-128 though, it is the square
root of that, so 2^-64 for a 50% risk of a clash, as the result
of the principle of the birthday attack.

Our goal is not to cover the World, but merely a zone of radio
transmissions, and we can adopt 118 bits of entropy with a risk
of 2^-59 of a clash.  We can then have 11e9 people use an average
of 46632982 devices each before we have a 50% risk of an identity
clash.  Given that this follows a
[binomial distribution](https://en.wikipedia.org/wiki/Binomial_distribution),
we should stay below half this, so 11e9 people using an average
of "only" 23316491 devices each.  I suppose *23316491 devices ought
to be enough for anyone*.

Identities form an order, and provided that we cover all frequencies
and none more than once, we can use 32 or 64 frequencies with
32! and 64! identities, respectively.  For 32 frequencies, we then
have 263130836933693530167218012160000000 choices or 118 bits of
entopy; for 64 frequencies, we would have had
126886932185884164103433389335161480802865516174545192198801894375214704230400000000000000
choices or 296 bits of entropy, well over a meaningful range.

Note that we do not limit our FFT to 32 frequencies; it is still
possible to encode multiple frequencies but form 32 groups that
act in unison.  Having more signals helps to increase receiver
sensitivity, but it does not expand the range of identities.


## Automatic Derivation of Identity

It is assumed that context, including higher-layer protocols,
will exchange the identities used in the following OrthoMod ideas
of channel identity.  The derivation of channel identities from this
information is one-directional, and cannot necessarily be reversed.

First and foremost, it is quite possible to create a random identity
from scratch.  The risks of clashes are as low as computed above, and
therefore sufficient for the purpose of OrthoMod radio transmissions.
It suffices to produce 118 bits of entropy, more is not problematic
but less increases the risk of clashes.

Second, a number of derived forms can also be imagined.  These would
apply to radio amateurs that use their call signs.  In this case,
clashes are prevented due to the global allocation scheme for unique
names.  OrthoMod does not require call signs anywhere, and facilitates
the random forms at the same level of functionality.  The representation
of the call sign in its smallest UTF-8 form is used to identify a
radio amateur, plus a dash and decimal number to identify a station,
with 0 as the default station, but still mentioned explicitly.  For
PA1RVR, the complete default code is then the string "PA1RVR-0".

In both cases, the code would designate an end point, not a channel.
When communication is sent outside of a connection, then the identity
for the OrthoMod frequency hopping identity is the SHA256 output of
the bytes for the end point designation.  This includes the messages
that request a new connection to be created, because their sender is
not yet known to the recipient for the request.

Channels that are used during a connection, including responses that
acknowledge a connection request and ones that terminate a connection,
are sent from an end point whose designation should be known at the
recipient.  For that reason, they can be sent with another channel
identity, leaving room for other unconnected messages.  The new
channel identity consists of the SHA256 of the transmitter rotated
over half of its byte length, XORed with the SHA256 of the receiver
which has not been rotated.  Note how the channel identities differ,
but are merely a byte-rotated version of one another. 


## Frequency Hopping for an Identity

Given an identity, we need to derive a frequency hopping scheme
from the SHA256 outputs.  In all cases, we use div/mod arithmetic
applied to the whole number.  We will only use the initial 16 bytes
or 128 bits, and split it into 32-bit words in big-endian order
that we div/mod with a number of values.  Note that SHA256 also
uses 32-bit math and big-endian order.  When a remainder exists,
it is ignored; the ranges are have about 2.5 bits to spare to
distribute the entropy reasonly well.

The first choice covers 32 options, the next 31 and so on, until
we reach 2 choices only.

  * UINT32 #0 is div-modded by 32, 31, 29, 28, 27, 6, 5 (entropy 29.281 bits)
  * UINT32 #1 is div-modded by 26, 25, 24, 23, 22, 21, 4 (entropy 29.305 bits)
  * UINT32 #2 is div-modded by 20, 19, 18, 17, 16, 15, 14, 2 (entropy 29.541 bits)
  * UINT32 #3 is div-modded by 30, 13, 12, 11, 10, 9, 8, 7, 3 (entropy 29.536 bits)

Some of these values are manually redistributed: 30 and 6..2;
this helps to keep the bit usage in a small [29.28;29.55] range
and the low values at the end benefit maximally from the little
remaining entropy because they wrap most often.  The downside
of this entropy optimisation is a slight complication in deriving
the frequency model, which is only needed once per data link.

At every stage, there is a list of frequencies (or frequency groups),
ranging from low to high.  Initially, this starts with `freq.0` and
ends with `freq.31` to give it a few symbolic names.

Every choice selects a value from that list, and removes it.  The
div-modded value used is indicated by the number of entries left.
The last remaining value is concatenated to the output list.

**Code:** See [split118.py](../models/split118.py) for numbers.


### Example Identification

Let's say PA1RVR is about to transmit from station 3 to station 12.
The stations bear designations "PA1RVR-3" and "PA1RVR-12", with the
following SHA256 values in hex notation:


  * `133c3709ac69e5ae87cb15e5dddab8fe34c5da885fd2823fce68162e0e9bf18c`
  * `54ec8b03b89751453bc50c076e602c4328cd3f384fdb982618631edc89beac8a`

The rotated channel identities, used to blend in the transmitter, are:

  * `34c5da885fd2823fce68162e0e9bf18c133c3709ac69e5ae87cb15e5dddab8fe`
  * `28cd3f384fdb982618631edc89beac8a54ec8b03b89751453bc50c076e602c43`

We shall XOR the binary values below the hex, take the first half,
split it into big-endian values of 32 bits and call the result our
channel identity.  We then obtain the frequency hopping scheme that
matches this channel identity.

When PA1RVR-3 transmits to PA1RVR-12, the channel identity is, depending
on the form you prefer:

  * `6029518be745d37af5ad1a2960fbddcf`
  * 0x6029518b, 0xe745d37a, 0xf5ad1a29, 0x60fbddcf
  * 1613320587, 3880113018, 4121762345, 1627119055

and the corresponding frequency hopping plan is:

  * 11, 7, 27, 13, 28, 4, 2, 21, 6, 5, 19, 15, 10, 0, 29, 26, 16, 23, 18, 3, 1, 30, 22, 9, 31, 12, 17, 20, 25, 8, 14, 24.

When PA1RVR-12 transmits to PA1RVR-3, the channel identity is, depending
on the form you prefer:

  * `3bf10831e3b27d889fa80b3954641474`
  * 0x3bf10831, 0xe3b27d88, 0x9fa80b39, 0x54641474
  * 1005652017, 3820125576, 2678590265, 1415844980

and the corresponding frequency hopping plan is:

  * 17, 3, 22, 10, 15, 7, 26, 8, 28, 30, 29, 0, 9, 23, 21, 19, 20, 31, 24, 16, 27, 14, 4, 12, 2, 11, 18, 6, 25, 13, 1, 5.

**Code:** See [freqhop.py](../models/freqhop.py) for a demonstration,
callable with the designations for a transmitter and receiver.


## Alternative Computations

We might consider more frequencies, and not using all of them.  Especially
due to the factorial effect we gain big time:

  * On 32 frequencies, 32 choices give 32!/(32-32)! = 118 bits of entropy
  * On 64 frequencies, 20 choices give 64!/(64-20)! = 115 bits of entropy
  * On 128 frequencies, 16 choices give 128!/(128-16)! = 111 bits of entropy
  * On 256 frequencies, 14 choices give 256!/(256-14)! = 111 bits of entropy
  * On 512 frequencies, 13 choices give 512!/(512-13)! = 117 bits of entropy

Of course, we need to relate this to the number of frequencies, and what
they do to the ratio of total bandwidth and available bandwidth per channel.
Furthermore, for orthogonal transmission the clash rate is important.
We shall need to figure out how to strike this new balance.
