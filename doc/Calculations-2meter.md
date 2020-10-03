# OrthoMod on the 2-meter Band

> *How well would OrthoMod perform on the 2-meter band?*

**TODO:** *Power in dB may be off.  Difficult and new.*

The
[2-meter band]
is popular among radio amateurs.  At a few watts of
transmitted power, the local range is good and the
transmission is reliable.  At more watts, a few
hundreds of kilometers can be reached.

The
[Dutch allocation to radio amateurs](https://wetten.overheid.nl/BWBR0036375/2017-04-01#Bijlagen)
for this band ranges from 144.0 Mhz to 146.0 Mhz
and transmission is supported up to 400 Watts with
a Full license, or 25 Watts with a Novice license,
both as primary user.  It is used for many things
and transmitting under the noise floor may be very
interesting to try on this band.


## Allocation of Frequency Bands

As long as we stay under the noise floor, we can
consider allocation of the entire band, at a
width of 2.0 Mhz and divide it into 32 sub-bands
of 62.5 kHz each.  We now know our maximum symbol
rate 62500 sym/s, and with NRZI/BPSK or TPSK
we can get a data rate **up to 62500 bps**.  Each
bit would be transmitted in 2304 to 2336 RF cycles.

Sub-bands of 62,5 kHz width would start at:

  * 144,000,000 Hz
  * 144,062,500 Hz
  * 133,125,000 Hz
  * ...
  * 145,937,500 Hz

We do not need to be louder than other signals,
nor de we need the factor 32 (or 30 dB) power
ratio; we need to be louder than other signals
on several of these frequencies, but not
necessarily on all, due to the certainty-weight
combination principle in the
[probabilistic detection](ProbabilisticDetection.md).
We may even refrain from transmission on occopied
bands (listen-before-you-send principle) and
simply skip those.

Of course, when all bands are actively overruling
our traffic than nothing may pass through until
some of the traffic gets more quiet.  Waiting is
the only solution then, for sub-noise signaling.
The long range and high power work against us here!

### Parallel Transmissions

We could treat the bands as a single band of
62,500 kbps or, in view of the fact that we already
need FFT to split the bands and that we can easily
add more frequencies, we might split it.  As an
example, we might define 25 frequencies at 2500 bps.
This would bring the total number of frequencies to
800, and the FFT would operate on 1024 frequencies
and reach up to 146,560,000 Hz.

The extra 224 frequencies would be transmitted as
zeroes and this can helps with filtering.  Both
NRZI/BPSK and TPSK are impartial to constant
phase changes (as a result of sharp filtering)
so it does not matter much in terms of phase change,
but it may be helpful in terms of dropping amplitude
near the end of the range.


## Transmission Power

We might go 30 dB below the noise floor.  We also
get some help from the repetitive signal, though.
In 2304 cycles, we have another gain of 67 dB, on
top of the 30 dB for 32-fold replication.  At a
gain of 97 dB we have a really sensitive solution,
at least in theory.  It raises the question how
fast our FFT can be.  It may well cover more periods *k*
but scaling at *k.N.log(k.N)* it may be more comfortable
to make more FFT runs, and get *k.N.log(N)* scaling.

We may now compete with a single nearby transmitter
at 400 W, with a transmitter that is 97 dB lower,
so 5 mW!  This is very much in theory of course, but
it appears that we can trade FFT computations for
tranmission power.  In reality, a remote transmitter
is more likely to overrule us, and there could be
multiple acting up, so we should use more power.

In reality, we may be better off fighting noise and
not the highest transmitter powers.  Let's assume
a 0 dBm noise level, which translates to 1 mW.
We might go 97 dB under there even, and transmit at
13 uW?!?  **Silly numbers, and probably wrong!**
Anyhow, it looks like we can use very low transmission
powers on this band; OrthoMod redundancy is forgiving.

### Reaching for the Moon

Let's assume transmitting at 400 W.  That would be
112 dB above the noise level.  OrthoMod gain adds
97 db to get 209 dB.  This is very high, given that
it takes about 252 dB to bounce off the Moon in the
2-meter band.  We would also use a dish atenna for
that application, for instance 1 m diameter and
apperture efficiency 0.6 would yield a gain of 3.4 dB,
but a diameter of 5 m already has a gain of 31 dB.
The choice that remains is simply how fast you want
to talk to the man in the Moon, because we could also
reduce our symbol rate to 300 bps, and increase the
gain by another 46 dB.  We would be reaching for the
Moon at our leasure.

