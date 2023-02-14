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
cp raspastroweb.service ${INSTALL_DIR}
chmod +x ${INSTALL_DIR}/raspastro-web.py

# Add service config to start automatically
echo "Setting up RaspAstro Web to start as current user ${current_user}..."
sed -i 's/^User=.*/User='${current_user}'/' ${INSTALL_DIR}/raspastroweb.service
#sudo cp ${INSTALL_DIR}/raspastroweb.service /etc/systemd/system
#sudo chmod 644 /etc/systemd/system/raspastroweb.service
#sudo sytemctl daemon-reload
#sudo systemctl enable raspastroweb.service
#sudo systemctl start raspastroweb.service



echo "RaspAstro Web Installed!"
#echo "To start RaspAstro Web"
#echo "Change to ${INSTALL_DIR}: cd ${INSTALL_DIR}"
#echo "Run RaspAstro Web:  ./raspastro-web.py"

