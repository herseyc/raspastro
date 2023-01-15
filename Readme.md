# RaspAstro

Just a place to put some of my Raspberry Pi Astronomy Stuff


build_hubble2.sh - Updates the raspberry pi, configures GPSD, some RPi optimizations, and  installs indi-core, indi-3rdparty drivers and libraries, and phd2

install-indi-driver.sh - Installs an indi-3rdparty driver or library based on user input.  Helpful to adding new indi drivers after initial build.

## Install
```
mkdir -p ~/Projects
cd ~/Projects
git clone https://github.com/herseyc/raspastro.git
```

Set INDILIBRARIES and INDIDRIVERS in build_hubble2.sh
Cross your fingers...
```
./build_hubble2.sh
```

Visit my EAA and astronomy site at: http://www.suffolksky.com/


Shoutout to https://gitea.nouspiro.space/nou/astro-soft-build/ for the great scripts which helped get me going in the right direction.


