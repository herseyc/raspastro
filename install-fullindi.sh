#!/bin/bash
##################################################
# install-fullindi.sh
# Setting up my Raspberry Pi for EAA and Astrophotography
#
# Run install-raspastro-dependencies.sh to install
# required dependencies
#
# Get, Build, and Install INDI CORE
# Get, Build, and Install All INDI 3rd-Party Libs and Drivers
# Install indiwebmanager and set to start on boot
#
# Visit me at: http://www.suffolksky.com/
##################################################

#Set the build directory
BUILDDIR=Projects

#Set the log file
LOGFILE=~/$BUILDDIR/build-raspastro.log

# Set JOBS to 2 if Raspberry Pi has < 2 GB RAM
JOBS=4


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

echo "Cleaning up INDI Core cmake directory if it exist."
cd ~/${BUILDDIR}/build
[ -d "indi-core" ] && rm -rf indi-core

echo "Running cmake for indi-core..."
cmake -B ~/${BUILDDIR}/build/indi-core -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release ~/${BUILDDIR}/indi 

echo "Building and installing INDI Core..."
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
echo "Building all INDI 3rd-Party Libraries..."

echo "Cleaning up indi-3rd-party-libs cmake directory if it exist."
cd ~/${BUILDDIR}/build
[ -d "indi-3rdparty-libs" ] && rm -rf indi-3rdparty-libs

echo "Running cmake for indi-3rdparty-libs..."
cmake -B ~/${BUILDDIR}/build/indi-3rdpary-libs -DCMAKE_INSTALL_PREFIX=/usr -DBUILD_LIBS=1 -DCMAKE_BUILD_TYPE=Release ~/${BUILDDIR}/indi-3rdparty

echo "Building and installing indi-3rdparty-libs..."
cd ~/${BUILDDIR}/build/indi-3rdparty-libs
make clean
make -j ${JOBS}
sudo make install


##################################################
# Build INDI 3rd-Party Drivers defined in INDIDRIVERS
##################################################
echo "Building all INDI 3rd-Party Drivers..."

echo "Cleaning up indi-3rd-party-drivers cmake directory if it exist..."
cd ~/${BUILDDIR}/build
[ -d "indi-3rdparty-drivers" ] && rm -rf indi-3rdparty-drivers

echo "Running cmake for indi-3rdparty-drivers..."
cmake -B ~/${BUILDDIR}/build/indi-3rdparty-drivers -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release ~/${BUILDDIR}/indi-3rdparty

echo "Building and installing indi-3rdparty-drivers..."
cd ~/${BUILDDIR}/build/indi-3rdparty-drivers
make clean
make -j ${JOBS}
sudo make install

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

current_user="$(id -u -n)"
echo "Setting up INDI Web Manager to Start with current user ${current_user}..."
sed -i 's/^User=.*/User='${current_user}'/' indiwebmanager.service

sudo cp indiwebmanager.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/indiwebmanager.service
sudo systemctl daemon-reload
sudo systemctl enable indiwebmanager.service
echo "INDI Web Manager Should Now Start on Boot as user ${current_user}..."

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

