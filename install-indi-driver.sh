#!/bin/bash
#################################################################
# install_indi_driver.sh
#
# Build and install a single INDI Driver or Library
#
# Assumes all dependencies are met
# and indi-core is already built and installed
# 
# Prompt for driver/library to install
# Get or update indi-3rdparty from repository
# Check that driver/library is part of indi-3rdparty
# Build and install 3rd-party library
#
# Visit me at: http://www.suffolksky.com/
#################################################################

#Set JOBS to 2 for Raspberry Pi with < 4 GB RAM
JOBS=4

BUILDDIR=Projects

mkdir -p ~/${BUILDDIR}/build

echo "Enter the INDI 3rd-Party Package to Install: "
read INDIPKG

echo "Getting INDI 3rd-Party Drivers and Libraries..."
cd ~/${BUILDDIR}
[ ! -d "indi-3rdparty" ] && git clone --depth=1 https://github.com/indilib/indi-3rdparty
cd indi-3rdparty
git fetch origin

[ ! -d "${INDIPKG}" ] && { echo "No INDI 3rd-Party package: ${INDIPKG} found"; exit; }

echo "Building INDI: "${INDIPKG}

cmake -B ~/${BUILDDIR}/build/${INDIPKG} -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release ~/${BUILDDIR}/indi-3rdparty/${INDIPKG}
cd ~/${BUILDDIR}/build/${INDIPKG}

make clean
make -j ${JOBS}
sudo make install

echo "Done."
