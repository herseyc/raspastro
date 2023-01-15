# RaspAstro

Just a place to put some of my Raspberry Pi Astronomy Stuff

Visit my EAA and astronomy site at: http://www.suffolksky.com/

## Install
```
mkdir -p ~/Projects
cd ~/Projects
git clone https://github.com/herseyc/raspastro.git
```

In all scripts BUILDDIR is set to Projects by default so if you do the above it will already be set. This downloads the repositories to ~/Projects and does the work in ~/Projects/build 

### build_hubble2.sh
Updates the raspberry pi, configures GPSD, some RPi optimizations, and  installs indi-core, indi-3rdparty drivers and libraries, and phd2

Set BUILDDIR, LOGFILE, INDILIBRARIES and INDIDRIVERS in build_hubble2.sh
Set JOBS to 2 if Raspberry Pi has < 4 GB of RAM
Cross your fingers...
```
./build_hubble2.sh
```

### install-indi-driver.sh
Installs an indi-3rdparty driver or library based on user input.  Helpful to adding new indi drivers after initial build.

```
./install-indi-driver.sh
```

### install-kstars.sh
Build and Installs StellarSolver and KStars

Edit script to configure BUILDDIR and LOGFILE (or just use the defaults)
Set JOBS to 2 if Raspberry Pi has < 4 GB of RAM
```
./install-indi-driver.sh
```


Shoutout to https://gitea.nouspiro.space/nou/astro-soft-build/ for the great scripts which helped get me going in the right direction.


