#!/bin/bash
############################################################
# build-raspastro-pi.sh
#
# Run the dependency and install scripts in the correct order
# to build out the astronomy software and a Raspberry Pi
#
# Edit each of the install files and set the BUILDDIR and LOGFILE
# if required (if you are using ~/Projects then it should work as
# it is configured.
#
# If you are on a Raspberry Pi with < 4 GB of memory then
# change the JOBS in each install script to 2 or you will 
# have issues with the builds.
# (PHD2, StellarSolver, and KStars are especilly memory 
# greedy during the builds.)
#
# Make sure to add any indi 3rd-party libraries or drivers
# you want to install in to the arrays in install-indi.sh
#
# Visit my EAA site at http://www.suffolksky.com/
#
############################################################

########################
# Install Dependencies
########################
./install-raspastro-dependencies.sh

########################
# Apply Optimizations 
########################
./apply-optimizations.sh

########################
# Install GPSD 
########################
./install-gpsd.sh

########################
# Install INDI 
########################
./install-indi.sh

########################
# Install PHD2 
########################
./install-phd2.sh

########################
# Install StellarSolver and KStars 
########################
./install-kstars.sh

echo ""
echo ""
echo "Done! Clear Skies!"

exit
