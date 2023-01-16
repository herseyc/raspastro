#!/bin/bash
##########################################################
#
# install-gpsd.sh
# Install and Configure GPSD 
#
# Visit my EAA site at http://www.suffolksky.com/
##########################################################

# Start Code Block
{
##################################################
# GPSD Configuration
##################################################

echo "Installing GPSD..."
sudo apt -y install gpsd

echo "Writing GPSD Configuration to /etc/default/gpsd ..."
sudo sed -i 's/^DEVICES.*/DEVICES=\"\/dev\/ttyACM0\"/' /etc/default/gpsd
sudo sed -i 's/^GPSD_OPTIONS.*/GPSD_OPTIONS=\"-r -n -F \/var\/run\/gpsd.sock\"/' /etc/default/gpsd
sudo sed -i 's/^USBAUTO.*/USBAUTO=\"false\"/' /etc/default/gpsd

exit

# End Code Block
}  2>&1 | tee -a ${LOGFILE}

