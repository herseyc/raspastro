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
LOGFILE=~/$BUILDDIR/build-raspastro.log

# Set JOBS to 2 if Raspberry Pi has < 2 GB RAM
JOBS=4


# Start Code Block
{

echo "Build Directory = ${BUILDDIR}"
echo "Make Jobs = ${JOBS}"
echo "Log File = ${LOGFILE}"

##################################################
# Building PHD2
##################################################

echo "Build and Install PHD2"
cd ~/${BUILDDIR}

echo "Getting PHD2 source..."
[ ! -d "phd2" ] && git clone https://github.com/OpenPHDGuiding/phd2.git
cd phd2
git pull origin --no-rebase

echo "Clean up PHD2 cmake files if they exist..."
cd ~/${BUILDDIR}/build
[ -d "phd2" ] && rm -rf phd2

echo "Running cmake for PHD2..."
cmake -B ~/${BUILDDIR}/build/phd2 ~/${BUILDDIR}/phd2

echo "Building and installing PHD2..."
cd ~/${BUILDDIR}/build/phd2
make clean
make -j ${JOBS}
sudo make install

echo "PHD2 Installed."

exit

# End Code Block
}  2>&1 | tee -a ${LOGFILE}

