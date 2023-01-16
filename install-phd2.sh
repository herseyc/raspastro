#!/bin/bash
#########################################################
#
# install-phd2.sh
# Builds and Installs PHD2
#
# Visit my EAA site at http://www.suffolksky.com/
#########################################################

#Set the build directory
BUILDDIR=Projects

#Set the log file
LOGFILE=~/$BUILDDIR/build-hubble2.log

# Set JOBS to 2 if Raspberry Pi has < 2 GB RAM
JOBS=4


# Start Code Block
{

##################################################
# Building PHD2
##################################################

echo "Build PHD2 and Install"

# Moved dependencies to install-raspastro-dependencies.sh
#echo "Installing PHD2 Dependencies..."
#sudo apt-get install -y build-essential git cmake pkg-config \
# libwxgtk3.0-gtk3-dev wx-common wx3.0-i18n libindi-dev libnova-dev \
# gettext zlib1g-dev libx11-dev libcurl4-gnutls-dev

cd ~/${BUILDDIR}
echo "Getting PHD2 source..."
[ ! -d "phd2" ] && git clone https://github.com/OpenPHDGuiding/phd2.git
echo "Building PHD2..."
cd phd2
git pull origin --no-rebase
mkdir -p ~/${BUILDDIR}/build/phd2
cd ~/${BUILDDIR}/build/phd2
cmake ~/${BUILDDIR}/phd2
make clean
make -j ${JOBS}
sudo make install

exit

# End Code Block
}  2>&1 | tee -a ${LOGFILE}

