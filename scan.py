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


authorized = [
    88.3,
    89.3,
    90.1,
    90.7,
    91.3,
    92.1,
    92.7,
    93.3,
    93.9,
    94.5,
    # 95.3,
    96.1,
    96.9,
    97.7,
    98.5,
    99.3,
    100.1,
    100.7,
    101.3,
    102.1,
    102.7,
    103.3,
    104.1,
    104.9,
    105.7,
    106.5,
    # 107.1,
    107.7
]

found = []
ilegal = []
not_found = []
freqs = get_center_frecuencies(88e6, 2.4e6, 108e6)

sdr = RtlSdr()

sdr.sample_rate = 2.4e6
sdr.gain = 5

power = []
fr = []
pre_state = 0
count = 0
start = 0
end = 0
width = 0
# valores a ajustar
thr = 0.02
width_th = 20

for cf in freqs:
    sdr.center_freq = cf

    samples = sdr.read_samples(256*1024)
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
                    center = round((end+start)/2.0, 1)
                    print(count+1, center)
                    count += 1
                    found.append(center)
                    if not (center in authorized):
                        ilegal.append(center)
                width = 0
            pre_state = 0

        fr.append(f[k])
sdr.close()
print("ilegal:", ilegal)
for i in authorized:
    if not (i in found):
        not_found.append(i)
print("not_found", not_found)
