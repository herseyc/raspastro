#!/bin/bash
###############################
###############################
###############################
###############################
# THIS IS A WORK IN PROGRESS  #
###############################
###############################
###############################
###############################
##################################################
# install-iwm.sh
# Setting up my Raspberry Pi for EAA and Astrophotography
#
# Run install-raspastro-dependencies.sh to install
# required dependencies
#
# Install indiwebmanager and set to start on boot
#
# Visit me at: http://www.suffolksky.com/
##################################################
#Set the build directory
BUILDDIR=Projects

#Set the log file
LOGFILE=~/$BUILDDIR/build-raspastro.log

#Set Installation Direcotry
INSTALL_DIR="/var/www/indiwebmanager"

#Python binary location
PYTHON_BIN="/usr/bin/python3"

# Set JOBS to 2 if Raspberry Pi has < 2 GB RAM
JOBS=4

#Start Code Block
{

echo "Build Directory = ${BUILDDIR}"
echo "Make Jobs = ${JOBS}"
echo "Log File = ${LOGFILE}"

echo "Setting up Python virtaulenv in ${INSTALL_DIR}..."
current_user="$(id -u -n)"
sudo mkdir -p ${INSTALL_DIR}
sudo chown -R ${current_user} ${INSTALL_DIR}

[[ ! -d "${INSTALL_DIR}/virtualenv" ]] && mkdir "${INSTALL_DIR}/virtualenv"
chmod 775 "${INSTALL_DIR}/virtualenv"
if [ ! -d "${INSTALL_DIR}/virtualenv/raspastroweb" ]; then
    "${PYTHON_BIN}" -m venv "${INSTALL_DIR}/virtualenv/indiwebmanager"
fi

echo "Activating Virtual Environment..."
source "${INSTALL_DIR}/virtualenv/indiwebmanager/bin/activate"


##################################################
# Installing indiwebmanager
##################################################
echo "Installing INDI Web Manager..."
sudo pip install indiweb

cd ~/${BUILDDIR}
echo "Getting indiwebmanager source..."
[ ! -d "indiwebmanager" ] && git clone https://github.com/knro/indiwebmanager.git
cd ~/${BUILDDIR}/indiwebmanager
git pull origin --no-rebase

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
