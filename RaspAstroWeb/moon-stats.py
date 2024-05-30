#########################################################
# Get informaiton about the Moon                        #
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

luna = AstroData(obslat=gps_data[1], obslon=gps_data[2], obslev=gps_data[3], obshorizon=MY_HORIZON)

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

luna.moon_data = {}

print(f"Location: {gpslatdms} {gpslondms}")
print(f"Moon Rise/Sun Set for next {numdays}")

while day < numdays:
   moondate = utc_datetime + timedelta(days=day)
   print(day)
   display_date = moondate.strftime("%m/%d/%Y")
   print(f"Date: {display_date}")
   luna.obs.date = moondate
   luna.obs.horizon = "-0:34"
   luna.obs.pressure = 0
   luna.moon_info()

   local_human_next_moonrise = time_to_human(to_local(luna.moon_data['next_moonrise'].datetime()))
   local_human_next_moonset = time_to_human(to_local(luna.moon_data['next_moonset'].datetime()))
   print(f"Moon Rise: {local_human_next_moonrise}")
   print(f"Moon Phase: {luna.moon_data['moon_quarter']} {luna.moon_data['moon_phase_name']} %{luna.moon_data['moon_phase_percent']}")
   print(f"Moon Set: {local_human_next_moonset}")

   day = day+1

