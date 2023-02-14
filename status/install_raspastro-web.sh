#!/bin/bash
#############################################
# Installs RaspAstro Web to the INSTALL_DIR #
#############################################

INSTALL_DIR=/var/www/raspastro

echo "Installs RaspAstro Web to ${INSTALL_DIR}"
current_user="$(id -u -n)"
sudo mkdir -p ${INSTALL_DIR}
sudo chown ${current_user} ${INSTALL_DIR}


cp *.py ${INSTALL_DIR}
cp -R templates ${INSTALL_DIR}
cp -R static ${INSTALL_DIR}


# Add service config to start automatically

echo "RaspAstro Web Installed!"
echo "cd to ${INSTALL_DIR} and run python3 raspastro-web.py"

