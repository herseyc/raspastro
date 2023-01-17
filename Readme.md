# RaspAstro

Just a place to put some of my Raspberry Pi Astronomy Stuff

Visit my Electronicly Assisted Astronomy (EAA) and Astrophotography site at: http://www.suffolksky.com/


I am testing these scripts on Raspberry Pi 64-bit OS, but they should also work on Raspberry Pi 32-bit OS.

## Install
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

### install-fullindi.sh
Builds and installs indi core, all indi 3rd-party libraries and drivers, and indiwebmanager

Set BUILDDIR and LOGFILE in install-indi.sh
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


