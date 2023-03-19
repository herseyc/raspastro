# RaspAstro

Just a place to put some of my Raspberry Pi Astronomy Stuff

Base directory contains a set of scripts I use to build out my Raspberry Pi with the software necessary for Electronically Assisted Astronomy or EAA.

I am testing these scripts on Raspberry Pi 64-bit OS, but they should also work on Raspberry Pi 32-bit OS.

I have also tested RaspAstro on Libre Computer Renegade SBC running Armbian Jammy. 

## RaspAstroWeb
The RaspAstroWeb directory contains a python web application which displays interesting and useful Astronomical data about the Sun, Moon, and Planets.  Also provides information on the current location and path of the International Space Station (ISS) along with information about visible passes based on an observer's location.  There is information on Polaris and how Polaris should be oriented in a polar scope for a proper polar alignment in the Northern Hemisphere.

Visit my Electronically Assisted Astronomy (EAA) and Astrophotography site at: http://www.suffolksky.com/

## Clone the git repository
```
mkdir -p ~/Projects
cd ~/Projects
git clone https://github.com/herseyc/raspastro.git
cd ~/Projects/raspastro
```

In all scripts BUILDDIR is set to Projects by default so if you do the above it will already be set. This downloads the repositories to ~/Projects and does the work in ~/Projects/build 

### install-raspastro-dependencies.sh
If this is a new Raspberry Pi OS build you will need to install the dependencies.
```
./install-raspastro-dependencies.sh
```
This updates the Raspberry Pi and installs the dependencies for INDI, INDI 3rd-Party, PHD2, StellarSolver, and KStars,

### install-gpsd.sh
Installs and configures GPSD
```
./install-gpsd.sh
```

### install-indi.sh
Builds and installs indi-core, selected indi-3rdparty drivers and libraries, and indiwebmanager

Set BUILDDIR, LOGFILE, INDILIBRARIES and INDIDRIVERS in install-indi.sh
Set JOBS to 2 if Raspberry Pi has < 4 GB of RAM
Only install indi libraries and drivers set in INDILIBRARIES and INDIDRIVERS
Cross your fingers...
```
./install-indi.sh
```
I install libasi, libqhy, indi-asi, indi-qhy, indi-eqmod, and indi-gpsd since these are the indi drivers I need for my set up.  Just add the ones you need to INDILIBRARIES and INDIDRIVERS. OR you can use install-fullindi.sh to install ALL the INDI 3rd-Party Libraries and Drivers.

### install-fullindi.sh
Builds and installs indi core, all indi 3rd-party libraries and drivers, and indiwebmanager

Set BUILDDIR and LOGFILE in install-fullindi.sh
Set JOBS to 2 if Raspberry Pi has < 4 GB of RAM
Cross your fingers...
```
./install-fullindi.sh
```

### install-indi-driver.sh
Installs an indi-3rdparty driver or library based on user input.  Helpful to adding new indi drivers after initial build.

```
./install-indi-driver.sh
```

### install-phd2.sh
Builds and installs PHD2
```
./install-phd2.sh
```

### install-kstars.sh
Build and Installs StellarSolver and KStars

Edit script to configure BUILDDIR and LOGFILE (or just use the defaults)
Set JOBS to 2 if Raspberry Pi has < 4 GB of RAM
```
./install-kstars.sh
```


Shoutout to https://gitea.nouspiro.space/nou/astro-soft-build/ for the great scripts which helped get me going in the right direction.


