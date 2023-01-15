#!/bin/bash
##################################################
# build_hubble2.sh
# Setting up my Raspberry Pi for EAA and Astrophotography
#
# Updates Raspberry Pi
# Applies some Optimizations
# Installs and Configures GPSD
# Get, Build, and Install INDI CORE
# Get, Build, and Install INDI 3rd-Party Libs and Drivers
# Get, Build, and Install PHD2
#
# Visit me at: http://www.suffolksky.com/
##################################################

#Set the build directory
BUILDDIR=Projects

#Set the log file
LOGFILE=~/$BUILDDIR/build-hubble2.log

# Set JOBS to 2 if Raspberry Pi has < 2 GB RAM
JOBS=4

#Array of INDI Libraries to build
INDILIBRARIES=(
  libasi
  libqhy
)

#Array of INDI Drivers to build
INDIDRIVERS=(
   indi-asi
   indi-qhy
   indi-eqmod
   indi-gpsd
)

#Start Code Block
{

##################################################
# Update Raspberry Pi
##################################################
echo "Updating the Raspberry Pi..."
sudo apt update 
sudo apt -y upgrade 

##################################################
# OPTIMIZATIONS
##################################################
echo "Updating /etc/dphys-swapfile changing CONF_SWAPSIZE=2048"
sudo sed -i "s/^CONF_SWAPSIZE.*/CONF_SWAPSIZE=2048/" /etc/dphys-swapfile

echo "Stopping, setting up, and starting swap..."
sudo dphys-swapfile swapoff
sudo dphys-swapfile setup
sudo dphys-swapfile swapon

echo "Decreasing Swappiness..."
echo "vm.swappiness = 1" | sudo tee /etc/sysctl.d/90-swappiness.conf
sudo sysctl --system

##################################################
# GPSD Configuration
##################################################

echo "Installing GPSD..."
sudo apt -y install gpsd

echo "Writing GPSD Configuration to /etc/default/gpsd ..."
sudo sed -i 's/^DEVICES.*/DEVICES=\"\/dev\/ttyACM0\"/' /etc/default/gpsd
sudo sed -i 's/^GPSD_OPTIONS.*/GPSD_OPTIONS=\"-r -n -F \/var\/run\/gpsd.sock\"/' /etc/default/gpsd
sudo sed -i 's/^USBAUTO.*/USBAUTO=\"false\"/' /etc/default/gpsd

##################################################
# Building and Installing Software
##################################################
echo "Using directory ~/"${BUILDDIR}" to build software..."

echo "Making Build Directories..."
mkdir -p ~/${BUILDDIR}/build
cd ~/${BUILDDIR}

##################################################
# Many thanks to the code script found here:
# https://gitea.nouspiro.space/nou/astro-soft-build/
##################################################

##################################################
# Building Indi Core
##################################################
echo "Install INDI Core Dependencies..."
sudo apt-get install -y  git cdbs dkms cmake fxload libev-dev \
  libgps-dev libgsl-dev libraw-dev libusb-dev zlib1g-dev \
  libftdi-dev libgsl0-dev libjpeg-dev libkrb5-dev libnova-dev \
  libtiff-dev libfftw3-dev librtlsdr-dev libcfitsio-dev \
  libgphoto2-dev build-essential libusb-1.0-0-dev libdc1394-22-dev \
  libboost-regex-dev libcurl4-gnutls-dev libtheora-dev

echo "Build INDI Core"
echo "Getting INDI Core..."
cd ~/${BUILDDIR}
[ ! -d "indi" ] && git clone --depth 1 https://github.com/indilib/indi.git
cd indi
git pull origin

echo "Creating INDI Core Makefiles..."
cmake -B ~/${BUILDDIR}/build/indi-core -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release ~/${BUILDDIR}/indi 

echo "Building INDI Core..."
cd ~/${BUILDDIR}/build/indi-core
make clean
make -j ${JOBS}
sudo make install

##################################################
# Building Indi 3rd-Party Drivers
##################################################

echo "Install 3rd-Party Dependencies..."

sudo apt-get -y install libnova-dev libcfitsio-dev libusb-1.0-0-dev \
    zlib1g-dev libgsl-dev build-essential cmake git libjpeg-dev \
    libcurl4-gnutls-dev libtiff-dev libfftw3-dev libftdi-dev libgps-dev \
    libraw-dev libdc1394-22-dev libgphoto2-dev libboost-dev \
    libboost-regex-dev librtlsdr-dev liblimesuite-dev libftdi1-dev \ 
    libavcodec-dev libavdevice-dev libindi-dev

echo "Build INDI 3rd-Party Libraries and Drivers"
echo "Getting INDI 3rd-Party Libraries and Drivers..."
cd ~/${BUILDDIR}
[ ! -d "indi-3rdparty" ] && git clone --depth=1 https://github.com/indilib/indi-3rdparty
cd indi-3rdparty
git pull origin

##################################################
# Build INDI 3rd-Party Libraries defined in INDILIBRARIES
##################################################

for LIB in "${INDILIBRARIES[@]}"; do

   echo "Building INDI Lilbrary: "${LIB} 

   cmake -B ~/${BUILDDIR}/build/${LIB} -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release ~/${BUILDDIR}/indi-3rdparty/${LIB}

   cd ~/${BUILDDIR}/build/${LIB}
   make clean
   make -j ${JOBS}
   sudo make install

done

##################################################
# Build INDI 3rd-Party Drivers defined in INDIDRIVERS
##################################################

for DRIVER in "${INDIDRIVERS[@]}"; do

   echo "Building INDI Driver: "${DRIVER}

   cmake -B ~/${BUILDDIR}/build/${DRIVER} -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release ~/${BUILDDIR}/indi-3rdparty/${DRIVER}

   cd ~/${BUILDDIR}/build/${DRIVER}
   make clean
   make -j ${JOBS}
   sudo make install

done

##################################################
# Installing indiwebmanager
##################################################

cd ~/${BUILDDIR}
echo "Installing INDI Web Manager..."
sudo pip install indiweb

echo "Getting indiwebmanager source..."

[ ! -d "indiwebmanager" ] && git clone https://github.com/knro/indiwebmanager.git
cd ~/${BUILDDIR}/indiwebmanager
git pull origin

echo "Setting up INDI Web Manager to Start with Pi..."

sudo cp indiwebmanager.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/indiwebmanager.service
sudo systemctl daemon-reload
sudo systemctl enable indiwebmanager.service
echo "INDI Web Manager Should Now Start on Boot..."

##################################################
# Building PHD2
##################################################

echo "Build PHD2 and Install"

echo "Installing PHD2 Dependencies..."
sudo apt-get install -y build-essential git cmake pkg-config \
 libwxgtk3.0-gtk3-dev wx-common wx3.0-i18n libindi-dev libnova-dev \
 gettext zlib1g-dev libx11-dev libcurl4-gnutls-dev

cd ~/${BUILDDIR}
echo "Getting PHD2 source..."
[ ! -d "phd2" ] && git clone https://github.com/OpenPHDGuiding/phd2.git
echo "Building PHD2..."
cd phd2
git pull origin
mkdir -p ~/${BUILDDIR}/build/phd2
cd ~/${BUILDDIR}/build/phd2
cmake ~/${BUILDDIR}/phd2
make clean
make -j ${JOBS}
sudo make install

##################################################
# DONE
##################################################

echo ""
echo ""
echo "I think that should mostly do it..."
echo "Probably want to check things out and then reboot"

exit

# End Code Block
}  2>&1 | tee -a ${LOGFILE}

