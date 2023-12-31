from pylab import *
from rtlsdr import *
from time import sleep

sdr = RtlSdr()

# configure device

sdr.sample_rate = 2.4e6
sdr.center_freq = 95e6
sdr.gain = 4

samples = sdr.read_samples(64*1024)

sdr.close()

# use matplotlib to estimate and plot the PSD
power, freqs = psd(samples, NFFT=1024, Fs=sdr.sample_rate /
                   1e6, Fc=sdr.center_freq/1e6)


# print("samples:", len(samples))
# print("power:", len(power))
# print("freqs:", len(freqs))
# print("freqs:", freqs[0], freqs[-1])

clf()
plot(freqs, power)
xlabel('Frequency (MHz)')
ylabel('Relative power (dB)')

show()
