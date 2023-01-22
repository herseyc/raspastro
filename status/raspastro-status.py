#!/usr/bin/env python3
###############################################
# Get the status of the RaspAstro Pi
###############################################

from flask import Flask, render_template
from gevent.pywsgi import WSGIServer
import netifaces as ni

WEB_PORT = 5000
WEB_HOST = "0.0.0.0"


app = Flask(__name__)

@app.route('/')
def status():


   ip_addresses =  {}

#   networkinterfaces = ni.interfaces()
#   for interface in networkinterfaces:
#       ip_addresses[interface] = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']

#   eth0ip = ni.ifaddresses(address)[ni.AF_INET][0]['addr']
   wlan0ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

   # Display GPS Fix
   gpsfixtype = "PLACEHOLDER"
   templateData = {
      'interfaces' : wlan0ip,
      'gpsfixtype' : gpsfixtype
      }

   return render_template('./raspastrostatus.html', **templateData)

# app.run(host=WEB_HOST, port=WEB_PORT)
http_server = WSGIServer((WEB_HOST, WEB_PORT), app)
http_server.serve_forever()
