# sdr scanner 
> SDR scanner for pirate fm radios

This repo contains test scripts for sdr-rtl intended to work on many RPI located on remote locations

## Module Requirements
```bash
sudo pip3 install matplotlib
sudo pip3 install numpy
sudo pip3 install pyrtlsdr

```

## SDR Software requirements
```bash
sudo apt install rtl-sdr librtlsdr-dev

```

## SDR server for SDR over LAN
```bash
mkdir spyserver
cd spyserver

wget -O spyserver.tgz http://airspy.com/?ddownload=5795
tar xvzf spyserver.tgz
```