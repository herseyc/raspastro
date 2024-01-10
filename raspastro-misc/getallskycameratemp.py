#!/usr/bin/env python3
###########################################
#
# External Temperature Script for indi-allsky
# Configured on indi-allsky Camera Page
# Uses adafruit-circuitpython-dht
#
# Test:
# TEMP_JSON=/tmp/foobar ./getallskycameratemp.py
# Check /tmp/foobar for JSON output
#
###########################################
import os
import sys
import io
import json
import board
import adafruit_dht

# Initialize DHT Device
# This is for a DHT11 connected to GPIO4
dhtDevice = adafruit_dht.DHT11(board.D4)

# Get the Temperature in C
temperature = dhtDevice.temperature

# Make sure the TEMP_JSON environment variable exist
try:
    # data file is communicated via environment variable
    temp_json = os.environ['TEMP_JSON']
except KeyError:
    # Exit the dhtDevice
    dht.Device.exit()
    # Exit 1
    sys.exit(1)

# Dictionary file for JSON
temp_data = {
   'temp' : temperature
}

# write json data TEMP_JSON
with io.open(temp_json, 'w') as f_temp_json:
    json.dump(temp_data, f_temp_json, indent=4)


# Exit the dhtDevice
dhtDevice.exit()

# Success Exit 0
sys.exit(0)

