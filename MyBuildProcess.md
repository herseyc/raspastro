#Building my Raspberry Pi

Just documenting how I build a Raspberry Pi for EAA

## Raspberry Pi OS
Using the Raspberry Pi Imager https://www.raspberrypi.com/software/ I write the Raspberry Pi 64-bit OS to my SD Card

After the OS is written to the SD Card, put the card in the Raspberry Pi and boot the Raspberry Pi connected to a monitor, keyboard, and mouse.

Do all the initial configuratoins:
- Language and Keyboard
- Username and password
- Wifi
- Etc...

Once the initial configuration is completed run the Raspberry Pi Configuration from the Preference menu.  
- From the System menu I set the Hostname.  
- From the Interfaces menu I enable SSH and VNC
- From the Performance menu I set GPU Memory to 16


Then reboot.

## Getting the raspastro scirpts

SSH is now enabled so I ssh into the Raspberry Pi and git my my scripts from raspastro

```
apt install -y git 
mkdir -p ~\Projects
cd ~\Projects
git clone https://github.com/herseyc/raspastro.git
cd ~/Projects/raspastro
```

## Installing EAA Software

First I update the Raspberry Pi and install the dependencies
```
./install-raspastro-dependencies.sh
```

Then I apply the OS Optimizations
```
./apply-optimizations.sh
```

Install and Configure GPSD
```
./install-gpsd.sh
```

I edit the install-indi.sh script and make sure all the indi 3rd-party libraries and drivers I want to install are assigned and then run install-indi.sh
```
./install-indi.sh
```



