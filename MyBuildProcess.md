# Building my Raspberry Pi

Just documenting the process I use to build a Raspberry Pi for EAA using the RaspAstro scripts

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

## Set Up the Raspberry Pi
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

## Installing EAA Software

### Build and Install INDI
I edit the install-indi.sh script and make sure all the indi 3rd-party libraries and drivers I want to install are assigned and then install indi and the selected 3rd-party libraries and drivers.
```
./install-indi.sh
```
OR if I want to install all the INDI 3rd-Party Libraries and Drivers I just run
```
./install-fullindi.sh
```

## Build and Install PHD2
Run the script to build and install PHD2
```
./install-phd2.sh
```

## Build and Install StellarSolver and Kstars
Run the script to build and install StellarSolver and then KStars
```
./install-kstars.sh
```

A
A


