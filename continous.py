from pylab import *
from rtlsdr import *
import matplotlib.animation as animation


def update_plot(i):
    samples = sdr.read_samples(256*1024)
    ax.clear()
    Pxx, freqs = psd(samples, NFFT=1024, Fs=sdr.sample_rate /
                     1e6, Fc=sdr.center_freq/1e6)
    ax.plot(freqs, 10*np.log10(Pxx))
    ax.set_xlabel('Frequency (MHz)')
    ax.set_ylabel('Relative power (dB)')
    ax.set_title('Real-time PSD')
    ax.set_xlim(91, 95)  # Adjust the x-axis range as needed


sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 93e6
sdr.gain = 4

fig, ax = plt.subplots()

# Update every 1000ms (1 second)
ani = animation.FuncAnimation(fig, update_plot, interval=1000)
plt.show()

sdr.close()
