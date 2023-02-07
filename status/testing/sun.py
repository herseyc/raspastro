from datetime import datetime
from dateutil import tz
import requests

MY_LAT = 36.7794571 # Your latitude
MY_LON = -76.5355366 # Your longitude


def to_local(time):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    time = time.replace(tzinfo=from_zone)
    local_time = time.astimezone(to_zone)
    return local_time



def is_at_night(checkdate, lat, lon):
    '''
    determine if UTC (checkdate) for location (lat, lon) is daytime
    or nighttime in local time based on Sunrise-Sunset.org API
    return True if nighttime, False if daytime 
    '''
    #Get sunrise/sunset for UTC checkdate from Sunrise-Sunset.org API
    fordate = f"{checkdate.year}-{checkdate.month}-{checkdate.day}"
    # Set up parameters for Sunrise-Sunset.org API Request
    parameters = {
        "lat": lat,
        "lng": lon,
        "formatted": 0,
        "date": fordate
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    # Convert sunrise and sunset time from UTC to local time
    # and get minutes since midnight
    local_sunrise = to_local(datetime.fromisoformat(data["results"]["sunrise"]))
    local_sunrise_min = (local_sunrise.hour * 60) + local_sunrise.minute
    local_sunset = to_local(datetime.fromisoformat(data["results"]["sunset"]))
    local_sunset_min = (local_sunset.hour * 60) + local_sunset.minute
    
    # convert UTC to local time
    local_checkdate = to_local(checkdate)
    # get local minutes since midnight
    local_checkdate_min = (local_checkdate.hour * 60) + local_checkdate.minute

    if  local_sunset_min > local_checkdate_min  > local_sunrise_min:
        return False
    else:
        return True

# Test
checkdate = datetime.fromisoformat("2023-02-09 01:33:50.364767")
print(checkdate)
is_night = is_at_night(checkdate, MY_LAT, MY_LON)
if is_night:
   print("Nighttime")
else:
   print("Daytime")

checkdate = datetime.fromisoformat("2023-02-09 15:33:50.364767")
print(checkdate)
is_night = is_at_night(checkdate, MY_LAT, MY_LON)
if is_night:
   print("Nighttime")
else:
   print("Daytime")
