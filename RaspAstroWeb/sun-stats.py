#########################################################
# Get informaiton about the Sun                         #
#########################################################
import numpy
from datetime import datetime, timedelta, timezone
from raspastroinfo import AstroData
import matplotlib as mpl
import matplotlib.pyplot as plt
from gps3 import agps3
from rasp_calc_func import *
from config import *
from get_gps import *
import time


gps_data_tuple = get_gps_data()

gpsfixtype = gps_data_tuple[0]
gpslatdms = gps_data_tuple[1]
gpslondms = gps_data_tuple[2]
gpsaltitude = gps_data_tuple[3]
gpslatitude = gps_data_tuple[4]
gpslongitude = gps_data_tuple[5]
gps_data = gps_data_tuple[6]

sol = AstroData(obslat=gps_data[1], obslon=gps_data[2], obslev=gps_data[3], obshorizon=MY_HORIZON)

# number of days to compute
numdays = 7
day = 0

#Get local time offset
timeoffset = datetime.now() - datetime.utcnow()
timeoffsetsec = int(round(timeoffset.total_seconds() / 3600))
#print(timeoffsetsec)

#Set time to today at midnight
today_midnight = datetime.now().replace(hour=0, minute=0)
#print(today_midnight)

#convert today at midnight to UTC
utc_datetime = today_midnight - timeoffset
#print(utc_datetime)

sol.sun_data = {}

print(f"Sun Rise/Sun Set for next {numdays}")

while day < numdays:
   sundate = utc_datetime + timedelta(days=day)
   print(day)
   display_date = sundate.strftime("%m/%d/%Y")
   print(f"Date: {display_date}")
   sol.obs.date = sundate
   sol.sun_info()

   local_human_next_sunrise = time_to_human(to_local(sol.sun_data['next_sunrise'].datetime()))
   local_human_next_sunset = time_to_human(to_local(sol.sun_data['next_sunset'].datetime()))
   print(f"Sunrise: {local_human_next_sunrise}")
   print(f"Sunset: {local_human_next_sunset}")

   #Compute the length of the day
   day_length = sol.sun_data['next_sunset'].datetime() - sol.sun_data['next_sunrise'].datetime() 
   print(f"Day Length: {day_length}")

   day = day+1

