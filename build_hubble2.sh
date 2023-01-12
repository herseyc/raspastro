#!/bin/bash

#Set the build directory

BUILDDIR=build-pi

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
echo "Writing GPSD Configuration to /etc/default/gpsd ..."
sudo sed -i 's/^DEVICES.*/DEVICES=\"\/dev\/ttyACM0\"/' /etc/default/gpsd
sudo sed -i 's/^GPSD_OPTIONS.*/GPSD_OPTIONS=\"-r -n -F \/var\/run\/gpsd.sock\"/' /etc/default/gpsd
sudo sed -i 's/^USBAUTO.*/USBAUTO=\"false\"/' /etc/default/gpsd

##################################################
# Building and Installing Software
##################################################
echo "Using directory ~/"${BUILDDIR}" to build software..."

echo "Making Build Directory..."
mkdir -p ~/${BUILDDIR}

cd ~/${BUILDDIR}

##################################################
# ZWO ASI and EAF SDK
##################################################
echo "Download and Install ASI SDKs"

echo "Downloading and Installing ASI Camera SDK..."
wget -O ASI-Camera-SDK.tar.bz2 'https://dl.zwoastro.com/software?app=AsiCameraDriverSdk&platform=macIntel&region=Overseas'

tar xvf ASI-Camera-SDK.tar.bz2

cd ~/${BUILDDIR}/ASI_linux_mac_SDK*/lib
sudo cp ./armv7/libASICamera2.so.* /usr/local/lib
sudo install asi.rules /lib/udev/rules.d

echo "Downloading and Installing ASI EAF SDK..."
wget -O ASI-EAF-SDK.tar.bz2 'https://dl.zwoastro.com/software?app=EafSdk&platform=linux&region=Overseas'
 
tar xvf ASI-EAF-SDK.tar.bz2

cd ~/${BUILDDIR}/EAF_linux_mac_SDK*/lib
sudo cp ./armv7/libEAFFocuser.so.* /usr/local/lib
sudo install eaf.rules /lib/udev/rules.d

echo "Create Links for ASI SDK Libraries..."
cd /usr/local/lib
sudo ln -s libASICamera2.so.* libASICamera2.so
sudo ln -s libEAFFocuser.so.* libEAFFocuser.so

##################################################
# Building Indi Core
##################################################


cd ~/${BUILDDIR}

echo "Install INDI Core Dependencies..."
sudo apt-get install -y  git cdbs dkms cmake fxload libev-dev \
  libgps-dev libgsl-dev libraw-dev libusb-dev zlib1g-dev \
  libftdi-dev libgsl0-dev libjpeg-dev libkrb5-dev libnova-dev \
  libtiff-dev libfftw3-dev librtlsdr-dev libcfitsio-dev \
  libgphoto2-dev build-essential libusb-1.0-0-dev libdc1394-22-dev \
  libboost-regex-dev libcurl4-gnutls-dev libtheora-dev

echo "Build INDI Core"
echo "Getting INDI Core..."
mkdir -p ~/${BUILDDIR}/Projects
cd ~/${BUILDDIR}/Projects
git clone --depth 1 https://github.com/indilib/indi.git

echo "Making INDI Core..."
mkdir -p ~/${BUILDDIR}/Projects/build/indi-core
cd ~/${BUILDDIR}/Projects/build/indi-core
cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/${BUILDDIR}/Projects/indi
make -j4
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
    libavcodec-dev libavdevice-dev

sudo apt-get -y install libindi-dev

echo "Build INDI 3rd-Party Libraries and Drivers"
echo "Getting INDI 3rd-Party Drivers..."
cd ~/${BUILDDIR}/Projects
git clone --depth=1 https://github.com/indilib/indi-3rdparty

##################################################
# Build INDI 3rd-Party Libraries defined in INDILIBRARIES
##################################################

for LIB in "${INDILIBRARIES[@]}"; do

   echo "Building INDI Lilbrary: "${LIB} 

   mkdir -p ~/${BUILDDIR}/Projects/build/${LIB}
   cd ~/${BUILDDIR}/Projects/build/${LIB}
   cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/${BUILDDIR}/Projects/indi-3rdparty/${LIB}
   make -j4
   sudo make install

done

##################################################
# Build INDI 3rd-Party Drivers defined in INDIDRIVERS
##################################################

for DRIVER in "${INDIDRIVERS[@]}"; do

   echo "Building INDI Driver: "${DRIVER}

   mkdir -p ~/${BUILDDIR}/Projects/build/${DRIVER}
   cd ~/${BUILDDIR}/Projects/build/${DRIVER}
   cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/${BUILDDIR}/Projects/indi-3rdparty/${DRIVER}
   make -j4
   sudo make install

done

##################################################
# Installing indiwebmanager
##################################################

cd ~/${BUILDDIR}
echo "Installing INDI Web Manager..."
sudo pip install indiweb

echo "Getting indiwebmanager source..."

git clone https://github.com/knro/indiwebmanager.git
cd ~/${BUILDDIR}/indiwebmanager

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
git clone https://github.com/OpenPHDGuiding/phd2.git
echo "Building PHD2..."
cd phd2
mkdir -p tmp
cd tmp
cmake ..
make
sudo make install

##################################################
# DONE
##################################################

echo ""
echo ""
echo "I think that should mostly do it..."
echo "Probably want to check things out and then reboot"



