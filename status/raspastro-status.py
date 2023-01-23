#!/usr/bin/env python3
###############################################
# Get the status of the RaspAstro Pi
###############################################

from flask import Flask, render_template
from gevent.pywsgi import WSGIServer
from gps3 import agps3
from time import sleep

WEB_PORT = 5000
WEB_HOST = "0.0.0.0"



app = Flask(__name__)



#@app.route('/')
#def main():
#    return render_template('main.html')


the_connection = agps3.GPSDSocket()
the_fix = agps3.DataStream()

the_connection.connect()
the_connection.watch()

print(f"GPS {the_fix}")

for new_data in the_connection:
   if new_data:
      the_fix.unpack(new_data)
      print(the_fix)

      gpsfixtype = the_fix.mode
      gpslatitude = the_fix.lat
      gpslongitude = the_fix.lon
      print(f"Fix: {gpsfixtype} Lat: {gpslatitude} Lon: {gpslongitude}")

   else:
      the_fix = agps3.DataStream()
      sleep(1)
