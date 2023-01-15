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
