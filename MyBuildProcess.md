# Building my Raspberry Pi for EAA

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

I disconnect the monitor, mouse, and keyboard. From here on I will be access the Raspberry Pi remotely over SSH or VNC. 

## Getting the raspastro scripts

After the reboot SSH will be enabled so I ssh into the Raspberry Pi and git my my scripts from raspastro
```
apt install -y git 
mkdir -p ~\Projects
cd ~\Projects
git clone https://github.com/herseyc/raspastro.git
cd ~/Projects/raspastro
```

I am building this on a Raspberry Pi 4B with 8 GB of memory.  If your Raspberry Pi has less than 4 GB of memory edit each of the install scripts and change JOBS=4 to JOBS=2.  

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
I use this GPS Module https://amzn.to/3CVOpLD 

## Installing EAA Software

### Build and Install INDI
I edit the install-indi.sh script and make sure all the indi 3rd-party libraries and drivers I want to install are assigned and then install indi and the selected 3rd-party libraries and drivers. This also installs the indiwebmanager interface.
```
./install-indi.sh
```
OR if I want to install all the INDI 3rd-Party Libraries and Drivers I just run
```
./install-fullindi.sh
```

After the indi build completes I can start the indiwebmanager and validate I can access it 
```
sudo systemctl start indiwebmanager.service
```
Then access the indiwebmanager at http://IPADDRESSofPI:8264

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



