#!/bin/bash

###################################################################
# Install the required dependencies for INDI, INDI-3rdParty
# PHD2, StellarSolve, and KStars
#
# I'll end up removing them from the individual scripts since
# there is a lot of overlap.  Will take a few runs of testing 
# before I am sure I got them all.
#
###################################################################
echo "Updating Raspberry Pi..."
sudo apt update
sudo apt -y upgrade

echo "Installing Dependencies..."
sudo apt -y install libnova-dev libcfitsio-dev libusb-1.0-0-dev \
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
        qml-module-qtquick-controls pkg-config libev-dev \
        cdbs dkms  fxload libusb-dev libgsl0-dev  libkrb5-dev \
	libtheora-dev libdc1394-22-dev libavcodec-dev libavdevice-dev \
	libindi-dev libwxgtk3.0-gtk3-dev wx-common wx3.0-i18n libx11-dev

echo "Installing python packages..."
sudo pip3 install netifaces gps3
exit
