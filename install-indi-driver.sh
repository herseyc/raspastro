#!/bin/bash

BUILDDIR = build-pi

echo "Enter the INDI 3rd-Party Package to Install: "
read INDIPKG


echo "Getting INDI 3rd-Party Drivers..."
cd ~/${BUILDDIR}/Projects
rm -rf indi-3rdparty
git clone --depth=1 https://github.com/indilib/indi-3rdparty

echo "Building INDI Lilbrary: "${INDIPKG}

mkdir -p ~/${BUILDDIR}/Projects/build/${INDIPKG}
cd ~/${BUILDDIR}/Projects/build/${INDIPKG}
cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/${BUILDDIR}/Projects/indi-3rdparty/${INDIPKG}
make -j4
sudo make install


