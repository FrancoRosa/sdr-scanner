#!/usr/bin/env python3

from pylab import *
from rtlsdr import *
from fm_freq import *
import datetime
from pathlib import Path

folder = "/home/pi/sdr-scanner/csv/"
current_date = datetime.datetime.now()
file = folder + current_date.strftime("%Y-%m")+".csv"
time = current_date.strftime("%m-%d %H:%M")


def file_exists(file_path):
    file_path_obj = Path(file_path)
    return file_path_obj.exists()


def build_headers():
    if not (file_exists(file)):
        headers = "timestamp"
        for f in authorized:
            headers = headers + ", %.1f" % f
        headers = headers + ", illegal, not found" + "\n"

        with open(file, 'w') as f:
            f.write(headers)

build_headers()

def get_center_frequencies(start, step, end):
    freqs = []
    target = start
    while target < end:
        freqs.append(target)
        target += step
    return freqs


found = []
illegal = []
not_found = []
c_freqs = get_center_frequencies(start=88e6, step=2.4e6, end=108e6)

sdr = RtlSdr()

sdr.sample_rate = 2.4e6
sdr.gain = sdr_gain

power = []
fr = []
pre_state = 0
count = 0
start = 0
end = 0
width = 0


for cf in c_freqs:
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
                        illegal.append(center)
                width = 0
            pre_state = 0

        fr.append(f[k])
sdr.close()

for i in authorized:
    if not (i in found):
        not_found.append(i)

log = time
for i in authorized:
    check = ', 0'
    if i in found:
        check = ', 1'
    log = log + check

with open(file, 'a') as f:
    f.write(log + ", %d, %d, %s\n" % (len(illegal), len(not_found), str(illegal).replace(",", " ")))

print("not_found:", not_found)
print("illegal:", illegal)
