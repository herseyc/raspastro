#!/usr/bin/env python3
###############################################
# Get the status of the RaspAstro Pi
###############################################

from flask import Flask, render_template
from gevent.pywsgi import WSGIServer
from gps3 import agps3
from time import sleep
from raspastroinfo import AstroData
from raspissinfo import ISSData

WEB_PORT = 5000
WEB_HOST = "0.0.0.0"


#app = Flask(__name__)

#@app.route('/')
#def main():
#    return render_template('main.html')


the_connection = agps3.GPSDSocket()
the_fix = agps3.DataStream()
the_connection.connect()
the_connection.watch()


for new_data in the_connection:
   if new_data:
      the_fix.unpack(new_data)
      gpsfixtype = the_fix.mode
      gpslatitude = the_fix.lat
      gpslongitude = the_fix.lon
      if the_fix.mode != "n/a":
         print(f"Fix: {gpsfixtype} Lat: {gpslatitude} Lon: {gpslongitude}")
         break
   else:
      print("Waiting...")
      sleep(1)

the_connection.close()

# Intialize AstroData with GPS lat and lon coordinates
astro = AstroData(obslat=gpslatitude, obslon=gpslongitude)
print(astro.obs.date)

# Get Moon Info
moon = astro.moon_info()
print(moon)

# Get Sun Info
sun = astro.sun_info()
print(sun)

# Initialize AstroData with GPS lat and lon coordinates
iss = ISSData(obslat=gpslatitude, obslon=gpslongitude)
print(iss.obs.date)

print(f"ISS Geocentric Lat: {iss.iss_telemetry.sublat}")
print(f"ISS Geocentric Lon: {iss.iss_telemetry.sublong}")
print(f"ISS Elevation: {round(iss.iss_telemetry.elevation / 1609, 2)} Miles")

# Get ISS Next Passes
iss_next_passes = iss.iss_passes(duration=3)
for i in iss_next_passes:
    print(i['aos'], i['los'])


