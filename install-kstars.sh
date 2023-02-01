#!/bin/bash
###############################################################
#
# install-kstars.sh
#
# Builds and Installs StellarSolver and KStars
#
# Install dependencies using install-raspastro-dependencies.sh
#
# Visit my EAA site at: http://www.suffolksky.com/
###############################################################

BUILDDIR=Projects
# Set JOBS to 2 if Raspberry Pi < 4GB RAM
JOBS=4
LOGFILE=~/${BUILDDIR}/build-raspastro.log

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
git pull origin --no-rebase

echo "Cleaning up stellarsolver cmake files if they exist..."
cd ~/${BUILDDIR}/build
[ -d "stellarsolver" ] && rm -rf stellarsolver

echo "Running cmake for stellarsolver..."
cmake -B ~/${BUILDDIR}/build/stellarsolver -DCMAKE_BUILD_TYPE=Release ~/${BUILDDIR}/stellarsolver

echo "Building and installing stellarsolver..."
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
git pull origin --no-rebase

echo "Cleaning up kstars cmake files if they exist..."
cd ~/${BUILDDIR}/build
[ -d "kstars" ] && rm -rf kstars

echo "Running cmake for kstars..."
cmake -B ~/${BUILDDIR}/build/kstars -DBUILD_TESTING=Off -DCMAKE_BUILD_TYPE=Release ~/${BUILDDIR}/kstars

echo "Building and installing kstars..."
cd ~/${BUILDDIR}/build/kstars
make clean
make -j ${JOBS}
sudo make install 

print "Done."
exit

# End Code Block
} 2>&1 | tee -a ${LOGFILE}
