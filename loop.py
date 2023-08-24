from pylab import *
from rtlsdr import *


def get_center_frecuencies(start, step, end):
    freqs = []
    target = start
    while target < end:
        freqs.append(target)
        target += step
    return freqs


def get_carriers(power, fr, th):
    t_p = []
    t_f = []
    for i in range(len(power)):
        print("_______________")
        print(power[1])
        print("_______________")
        if power[i] > th:
            t_p.append(power[i])
            t_f.append(fr[i])
    return t_f, t_p


freqs = get_center_frecuencies(88e6, 2.4e6, 108e6)

sdr = RtlSdr()

sdr.sample_rate = 2.4e6
sdr.gain = 4

power = []
fr = []
pre_state = 0
count = 0
start = 0
end = 0
thr = 0.01
width = 0
width_th = 20

for cf in freqs:
    sdr.center_freq = cf

    samples = sdr.read_samples(64*1024)
    p, f = psd(samples, NFFT=1024, Fs=sdr.sample_rate /
               1e6, Fc=sdr.center_freq/1e6)
    for k in range(len(p)):

        if p[k] > thr:
            power.append(1)

            if pre_state == 0:
                start = f[k]
            else:
                width += 1
            pre_state = 1
        else:
            power.append(0)
            if pre_state == 1:
                end = f[k]
                if width > width_th:
                    print("freq %d, " % count, '%.1f, ' % ((end+start)/2.0))
                    count += 1
                width = 0
            pre_state = 0

        fr.append(f[k])
sdr.close()
clf()
plot(fr, power)
xlabel('Frequency (MHz)')
ylabel('Relative power (dB)')

# x, y = get_carriers(power, fr, -40)
# for i in range(20):
#     print(x[i], y[i])
show()
