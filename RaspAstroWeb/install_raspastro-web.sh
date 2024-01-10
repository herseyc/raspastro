#!/bin/bash
#############################################
# Installs RaspAstro Web to the INSTALL_DIR #
#############################################

INSTALL_DIR="/var/www/raspastro"
PYTHON_BIN="/usr/bin/python3"

# Get Hostname
HOSTNAME=$(hostname)

echo "Installing RaspAstro Web to ${INSTALL_DIR}..."
current_user="$(id -u -n)"
sudo mkdir -p ${INSTALL_DIR}
sudo chown -R ${current_user} ${INSTALL_DIR}

if [ -f "${INSTALL_DIR}/config.py" ]; then
    echo "Found config.py in ${INSTALL_DIR}. Saving existing config.py to config.old"
    cp ${INSTALL_DIR}/config.py ${INSTALL_DIR}/config.old
fi

echo "Copying python files to ${INSTALL_DIR}..."
cp *.py ${INSTALL_DIR}
echo "Copying template directory to ${INSTALL_DIR}..."
cp -R templates ${INSTALL_DIR}
echo "Copying static directory to ${INSTALL_DIR}..."
cp -R static ${INSTALL_DIR}
echo "Copying xephemcat directory to ${INSTALL_DIR}..."
cp -R xephemcat ${INSTALL_DIR}
echo "Copying supporing files to ${INSTALL_DIR}..."
cp raspastroweb.service ${INSTALL_DIR}
echo "Making  ${INSTALL_DIR}/raspastro-web.py executable..."
chmod +x ${INSTALL_DIR}/raspastro-web.py

echo "Setting up the Python Virtual Enviornment..."
[[ ! -d "${INSTALL_DIR}/virtualenv" ]] && mkdir "${INSTALL_DIR}/virtualenv"
chmod 775 "${INSTALL_DIR}/virtualenv"
if [ ! -d "${INSTALL_DIR}/virtualenv/raspastroweb" ]; then
    "${PYTHON_BIN}" -m venv "${INSTALL_DIR}/virtualenv/raspastroweb"
fi

echo "Activating Virtual Environment..."
source "${INSTALL_DIR}/virtualenv/raspastroweb/bin/activate"

echo "Installing python module requirements..."
pip3 install --upgrade pip setuptools wheel
pip3 install -r "requirements.txt"

echo "Generating Solar System map..."
cd ${INSTALL_DIR}
${INSTALL_DIR}/virtualenv/raspastroweb/bin/python3 ./planets.py

echo "Updating raspastroweb.service..."
echo "Setting ${current_user} in raspastroweb.service..."
sed -i 's\^User=.*\User='${current_user}'\' ${INSTALL_DIR}/raspastroweb.service

echo "Updating paths to ${INSTALL_DIR} in raspastroweb.service..."
sed -i 's\INSTALLDIR\'${INSTALL_DIR}'\g' ${INSTALL_DIR}/raspastroweb.service
echo "Setting up RaspAstroWeb to start at boot..."
sudo cp ${INSTALL_DIR}/raspastroweb.service /etc/systemd/system
sudo chmod 644 /etc/systemd/system/raspastroweb.service
sudo systemctl daemon-reload
sudo systemctl enable raspastroweb.service
echo "Starting RaspAstroWeb..."
sudo systemctl start raspastroweb.service

echo "RaspAstro Web Installed in ${INSTALL_DIR}!"

echo "###############################################"
echo "RaspAstroWeb at  http://${HOSTNAME}.local:5000/"
echo "###############################################"
echo "Done!"

