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
```

tightvncserver - script to start, stop, restart tightvncserver
tightvncserver.service - Run tightvncserver at boot
novnc.service - Run noVNC at boot for HTML5 browser access to tightvncserver

