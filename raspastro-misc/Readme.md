# Misc RaspAstro Configurations
Miscellaneous configuration to support RaspAstro. 

## Samba
Share directories via smb

Install
```
sudo apt install samba cifs-utils smbclient
```
### smb.conf
Sample Samba configuration file to create share 
/etc/samba/smb.conf


## VNC
```
sudo apt-get install tightvncserver novnc
# Create the Self Signed SSL Certificate for noVNC
# I put novnc.pem  in /home/pi/novnc directory
openssl req -x509 -nodes -newkey rsa:2048 -keyout novnc.pem -out novnc.pem -days 365
```

### tightvncserver 
Script to start, stop, restart tightvncserver

Edit tightvncserver to update geometry/desktop/etc, copy tightvncserver to /usr/local/bin, and use chmod +x to make it executable
```
sudo cp tightvncserver /usr/local/bin
sudo chmod +x /usr/local/bin/tighvncserver
```

### tightvncserver.service 
Run tightvncserver at boot

Edit tightvncserver.service and update username and path if necessary.  Copy tightvncserver.service to /etc/systemd/system, run systemctl daemon-reload, and systemctl enable tightvncserver.service to start tightvncserver at boot.
```
sudo cp tightvncserver.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable tightvncserver.service
```

### novnc.service 
Run noVNC at boot for HTML5 browser access to tightvncserver

Edit novnc.service and update username and path if necessary.  Copy novnc.service to /etc/systemd/system, run systemctl daemon-reload, and systemctl enable novnc.service to start novnc at boot.
```
sudo cp novnc.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable novnc.service
```
