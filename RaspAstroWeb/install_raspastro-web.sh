#!/bin/bash
#############################################
# Installs RaspAstro Web to the INSTALL_DIR #
#############################################

INSTALL_DIR="/var/www/raspastro"

echo "Installing RaspAstro Web to ${INSTALL_DIR}"
current_user="$(id -u -n)"
sudo mkdir -p ${INSTALL_DIR}
sudo chown ${current_user} ${INSTALL_DIR}

if [ -f "${INSTALL_DIR}/config.py" ]; then
    echo "Found config.py in ${INSTALL_DIR}. Saving existing config.py to config.old"
    cp ${INSTALL_DIR}/config.py ${INSTALL_DIR}/config.old
fi

echo "Copying python files to ${INSTALL_DIR}"
cp *.py ${INSTALL_DIR}
echo "Copying template directory to ${INSTALL_DIR}"
cp -R templates ${INSTALL_DIR}
echo "Copying static directory to ${INSTALL_DIR}"
cp -R static ${INSTALL_DIR}
echo "Copying supporing files to ${INSTALL_DIR}"
cp raspastroweb.service ${INSTALL_DIR}
echo "Making  ${INSTALL_DIR}/raspastro-web.py executable."
chmod +x ${INSTALL_DIR}/raspastro-web.py

echo "RaspAstro Web Installed in ${INSTALL_DIR}!"

