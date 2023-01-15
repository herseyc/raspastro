#!/bin/bash

BUILDDIR=Projects
mkdir -p ~/${BUILDDIR}/build

echo "Enter the INDI 3rd-Party Package to Install: "
read INDIPKG

echo "Getting INDI 3rd-Party Drivers and Libraries..."
cd ~/${BUILDDIR}
[ ! -d "indi-3rdparty" ] && git clone --depth=1 https://github.com/indilib/indi-3rdparty
cd indi-3rdparty
git pull origin

[ ! -d "${INDIPKG}" ] && { echo "No INDI 3rd-Party package: ${INDIPKG} found"; exit; }

echo "Building INDI: "${INDIPKG}

cmake -B ~/${BUILDDIR}/build/${INDIPKG} -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release ~/${BUILDDIR}/indi-3rdparty/${INDIPKG}
cd ~/${BUILDDIR}/build/${INDIPKG}

make clean
make -j4
sudo make install

echo "Done."
