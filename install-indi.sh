#!/bin/bash
##################################################
# build_hubble2.sh
# Setting up my Raspberry Pi for EAA and Astrophotography
#
# Run install-raspastro-dependencies.sh to install
# required dependencies
#
# Get, Build, and Install INDI CORE
# Get, Build, and Install INDI 3rd-Party Libs and Drivers
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
# Building and Installing INDI Software
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
echo "Build INDI Core"
echo "Getting INDI Core..."
cd ~/${BUILDDIR}
[ ! -d "indi" ] && git clone --depth 1 https://github.com/indilib/indi.git
cd indi
git pull origin --no-rebase

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
echo "Build INDI 3rd-Party Libraries and Drivers"
echo "Getting INDI 3rd-Party Libraries and Drivers..."
cd ~/${BUILDDIR}
[ ! -d "indi-3rdparty" ] && git clone --depth=1 https://github.com/indilib/indi-3rdparty
cd indi-3rdparty
git pull origin --no-rebase

##################################################
# Build INDI 3rd-Party Libraries defined in INDILIBRARIES
##################################################
echo "Building INDI 3rd-Party Libraries..."
for LIB in "${INDILIBRARIES[@]}"; do

   echo "Building INDI Lilbrary: "${LIB} 

   cmake -B ~/${BUILDDIR}/build/${LIB} -DCMAKE_INSTALL_PREFIX=/usr -DBUILD_LIBS=1 -DCMAKE_BUILD_TYPE=Release ~/${BUILDDIR}/indi-3rdparty/${LIB}

   cd ~/${BUILDDIR}/build/${LIB}
   make clean
   make -j ${JOBS}
   sudo make install

done

##################################################
# Build INDI 3rd-Party Drivers defined in INDIDRIVERS
##################################################
echo "Building INDI 3rd-Party Drivers..."
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
echo "Installing INDI Web Manager..."
cd ~/${BUILDDIR}
sudo pip install indiweb

echo "Getting indiwebmanager source..."
[ ! -d "indiwebmanager" ] && git clone https://github.com/knro/indiwebmanager.git
cd ~/${BUILDDIR}/indiwebmanager
git pull origin --no-rebase

echo "Setting up INDI Web Manager to Start with Pi..."

sudo cp indiwebmanager.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/indiwebmanager.service
sudo systemctl daemon-reload
sudo systemctl enable indiwebmanager.service
echo "INDI Web Manager Should Now Start on Boot..."

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

