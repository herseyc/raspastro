# RaspAstro Web
Web application which display interesting and useful Astronomy data.  Information about the Sun, Moon, planets, and the ISS.

## requirements.txt
Install the required python modules.
```
pip3 install -r requirements.txt
```

## config.py 
Config.py contains all the user-defined settings.

User-defined settings:
```
# Number of days to calculate ISS Passes
PASSDAYS = 5

#If USE_INDI is False then INDI Server info will not be queried
USE_INDI = True

# INDI Web Manager API Endpoint
INDIWEBMANAGER_API_ENDPOINT = "http://localhost:8624"

# Define Observer Horizon in DMS
MY_HORIZON = "0:34:0"

# Set to True to use GPS, False to use user configured lat/lon/elev
USE_GPS = True

# If USE_GPS is False use the following for observer location
# Latitude and Longitude DMS string
MY_LAT = "36:46:46.0"
MY_LON = "-76:32:8.1"

# Observer Elevation (float in meters)
MY_ELEVATION = 7.7
```

## raspastro-web.py
Flash app to display data on webpage. 

Edit config.py with your configuration settings and then use install_raspastro-web.sh to copy into INSTALL_DIR (/var/www/raspastro is the default).  Then run raspastro-web.py
```
./install_raspastro-web.sh
cd /var/www/raspastro
python3 raspastro-web.py
```

Will listen on port 5000, so just access at http://ipofdevice:5000 

If config.py exists in the INSTALL_DIR (default /var/www/raspastro) a copy of it, config.old, is created by install_raspastro-web.sh

## raspastroweb.service
This can be used to set up systemd to start raspastro-web.py at boot.

Edit the file and udate the user and directory if required (default user is pi, default directory is /var/www/raspastro)
```
cd /var/www/raspastro
sudo cp raspastroweb.service /etc/systemd/system
sudo chmod 644 /etc/systemd/system/raspastroweb.service
suod systemctl daemon-reload
sudo systemctl enable raspastroweb.service
sudo systemctl start raspastroweb.service
```

## Example Observer Information
The Observer Page displays the Observer's location information. The location information is obtained from GPSD or from the manual configurations config.py.  The INDI information is updated from the INDI Web Manager API.  The Observer information is static and only updates if refreshed.  The INDI Information updates every 30 seconds. 

![RaspAstro Observer Page](https://github.com/herseyc/raspastro/blob/master/RaspAstroWeb/img/raspastro-observer-page.png?raw=true)

## Example Solar System Information
Sun, Moon, and Planet Data.  This information on this page is only updated when refreshed.

![RaspAstro Solar System Page](https://github.com/herseyc/raspastro/blob/master/RaspAstroWeb/img/raspastro-solarsystem-page.png?raw=true)

## Example ISS Information
![RaspAstro ISS Page](https://github.com/herseyc/raspastro/blob/master/RaspAstroWeb/img/raspastro-iss-page.png?raw=true)

## Example Polaris/Polar Alignment Information
![RaspAstro Polaris Page](https://github.com/herseyc/raspastro/blob/master/RaspAstroWeb/img/raspastro-polaris-page.png?raw=true)

## planets.py
Generates a Solar System Map. 

![RaspAstro Solar System Map](https://github.com/herseyc/raspastro/blob/master/RaspAstroWeb/static/planets.png?raw=true)


## raspissinfo.py
ISSData Class to get ISS current information and determine next passes for observer location.

## raspastroinfo.py
AstroData Class to get information related to the Sun and Moon for an oberserver location

## rasp_calc_func.py
Functions to convert UTC to local time (to_local(time)), convert meters to miles (meters_to_miles(meters)), and determine is a UTC datetime is at night in local time (is_at_night(checkdate, lat, lon) for a specific location.

## examples.py
Examples for using the ISSData Class and AstroData Class as well as the rasp_calc_func.py
