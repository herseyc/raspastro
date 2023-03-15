#!/bin/bash
##################################################################
#
# apply-optimizations.sh
# Increase swapfile size to 2048
# Decrease swappiness
#
# Visit my EAA site at http://www.suffolksky.com/
##################################################################

#Set the build directory
BUILDDIR=Projects

#Set the log file
LOGFILE=~/$BUILDDIR/build-raspastro.log

#Start Code Block
{

##################################################
# OPTIMIZATIONS
##################################################
echo "Updating /etc/dphys-swapfile changing CONF_SWAPSIZE=2048"
sudo sed -i "s/^CONF_SWAPSIZE.*/CONF_SWAPSIZE=2048/" /etc/dphys-swapfile

echo "Stopping, setting up, and starting swap..."
sudo dphys-swapfile swapoff
sudo dphys-swapfile setup
sudo dphys-swapfile swapon

echo "Decreasing Swappiness..."
echo "vm.swappiness = 1" | sudo tee /etc/sysctl.d/90-swappiness.conf
sudo sysctl --system

echo "Disable cups..."
sudo systemctl disable cups.service

echo "Disable Printer Applet..."
sudo mv /etc/xdg/autostart/print-applet.desktop /etc/xdg/print-applet.desktop

exit

# End Code Block
}  2>&1 | tee -a ${LOGFILE}



