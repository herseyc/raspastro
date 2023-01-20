###############################################
# Get the status of the RaspAstro Pi
###############################################

import netifaces as ni

eth0ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
print(f"LAN IP: {eth0ip}")  


wlan0ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
print(f"WAN IP: {wlan0ip}")  

# Display GPS Fix
print("GPS Fix")
print("Lat:")
print("Long:")


print("INDI Server Status:")


