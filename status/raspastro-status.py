###############################################
# Get the status of the RaspAstro Pi
###############################################

import netifaces as ni
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def status():
#   if ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']:
#      eth0ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

   if ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']:
      wlan0ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

   # Display GPS Fix
   gpsfixtype = "PLACEHOLDER"
   templateData = {
      'wlan0ip' : wlan0ip,
      'gpsfixtype' : gpsfixtype
      }

   return render_template('./raspastrostatus.html', **templateData)

app.run(host="0.0.0.0")
