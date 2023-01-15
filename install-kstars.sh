#!/bin/bash

BUILDDIR=Projects
# Set JOBS to 2 if Raspberry Pi < 4GB RAM
JOBS=4
LOGFILE=~/${BUILDDIR}/build-hubble2.log

# Start Code Block
{

echo "Build Directory = ${BUILDDIR}"
echo "Make Jobs = ${JOBS}"
echo "Log File = ${LOGFILE}"

echo "Making Build Directory..."
mkdir -p ~/${BUILDDIR}

############################################################
# Install Dependencies
############################################################
sudo apt update
sudo apt install libnova-dev libcfitsio-dev libusb-1.0-0-dev \
        zlib1g-dev libgsl-dev build-essential cmake git \
        libjpeg-dev libcurl4-gnutls-dev libtiff-dev libfftw3-dev \
        libftdi-dev libgps-dev libraw-dev libdc1394-dev libgphoto2-dev \
        libboost-dev libboost-regex-dev librtlsdr-dev liblimesuite-dev \
        libftdi1-dev libavcodec-dev libavdevice-dev libeigen3-dev \
        extra-cmake-modules libkf5plotting-dev libqt5svg5-dev \
        libkf5xmlgui-dev libkf5kio-dev kinit-dev libkf5newstuff-dev \
        libkf5doctools-dev libkf5notifications-dev \
        qtdeclarative5-dev libkf5crash-dev gettext libkf5notifyconfig-dev \
        wcslib-dev libqt5websockets5-dev xplanet xplanet-images \
        qt5keychain-dev libsecret-1-dev breeze-icon-theme \
        qml-module-qtquick-controls pkg-config libev-dev

############################################################
# Build and Install StellarSolver
############################################################
echo "Building StellarSolver..."

cd ~/${BUILDDIR}
[ ! -d "stellarsolver" ] && git clone --depth=1 https://github.com/rlancaste/stellarsolver.git
cd stellarsolver
git pull origin

cmake -B ~/${BUILDDIR}/build/stellarsolver ../stellarsolver -DCMAKE_BUILD_TYPE=Release
cd ~/${BUILDDIR}/build/stellarsolver
make clean
make -j ${JOBS}
sudo make install

############################################################
# Build and Install KStars
############################################################
echo "Building KStars..."

cd ~/${BUILDDIR}

[ ! -d "kstars" ] && git clone --depth=1 https://invent.kde.org/education/kstars.git
cd kstars
git pull origin

cmake -B ~/${BUILDDIR}/build/kstars -DBUILD_TESTING=Off ../kstars -DCMAKE_BUILD_TYPE=Release
cd ~/${BUILDDIR}/build/kstars
make clean
make -j ${JOBS}
sudo make install 

# End Code Block
} > >(tee ${LOGFILE}) 2>&1
