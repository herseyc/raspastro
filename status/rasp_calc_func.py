########################################################
# Just some different calculations for RaspAstro       #
########################################################
from dateutil import tz
from datetime import datetime
import requests

########################################
# function to convert UTC to localtime #
########################################
def to_local(time):
    '''
    Convert UTC (time) to local time
    Returns local time
    '''
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    time = time.replace(tzinfo=from_zone)
    local_time = time.astimezone(to_zone)
    return local_time

########################################
# function to convert Meters to Miles  #
########################################
def meters_to_miles(meters):
    '''
    Convert meters (meters) to miles
    Returns miles
    '''
    miles = round(meters / 1609, 2)
    return miles

###################################################
# function to check if UTC is a night local time  #
###################################################
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


def time_to_human(time):
     day = time.day
     month = time.month
     year = time.year
     hour = time.hour
     tod = ""
     if hour > 12:
        hour -= 12
        tod = "PM"
     elif hour == 12:
        tod = "PM"
     elif hour == 0:
        hour = 12
        tod = "AM"
     else:
        tod = "AM"
     minute = time.minute
     if minute < 10:
        minute = f"0{minute}"
     timezone = time.tzinfo
     tz = timezone.tzname(time)
     humantime = f"{month}/{day}/{year} {hour}:{minute} {tod} {tz}"
     return humantime

def convert_dd_to_dms(dd):
    degrees = int(dd)
    temp = 60 * (dd - degrees)
    minutes = int(temp)
    seconds = round(60 * (temp - minutes), 1)
    dms = f"{degrees}:{abs(minutes)}:{abs(seconds)}"
    return dms
 
