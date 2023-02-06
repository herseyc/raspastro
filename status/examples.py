# Examples using the RaspAstro classes
# AstroData (Moon, Sun, More to Come...) from ephem
from raspastroinfo import AstroData
# ISSData (ISS telemerty and pass information) using ephem
from raspissinfo import ISSData

from datetime import datetime
from dateutil import tz
import math

# function convert utc to local time
def to_local(time):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    time = time.replace(tzinfo=from_zone)
    local_time = time.astimezone(to_zone)
    return local_time

# function to convert Meters to Miles
def meters_to_miles(meters):
    miles = round(meters / 1609, 2)
    return miles


# Intialize AstroData 
# Optional Keyword args:
# obslat = Observer Latitude in DMS (Default: 36:43:41.538)
# obslon = Observers Longitude in DMS (Default: -76:35:0.8232)
# obsepoch = Observation Time in UTC (Default: datetime.utcnow()))
# obselev = Observers Elevation (Default: 3) (meters)

astro = AstroData()
print(astro.obs.date)

# Get Moon Info
moon = astro.moon_info()
print(moon)

# Get Sun Info
sun = astro.sun_info()
print(sun)

# Initialize ISSData 
# Optional Keyword args:
# obslat = Observer Latitude in DMS(Default: 36:43:41.538)
# obslon = Observers Longitude in DMS(Default: -76:35:0.8232)
# obsepoch = Observation Time in UTC (Default: datetime.utcnow()))
# obselev = Observers Elevation (Default: 3) (meters)
iss = ISSData()
print(iss.obs.date)
print(f"Observer lat: {iss.obs.lat}")
print(f"Observer lon: {iss.obs.lon}")
print(f"Observer horizon: {iss.obs.horizon}")
print(iss.iss_module_name)
print(iss.iss_tle1)
print(iss.iss_tle2)

print(f"ISS Eclipsed: {iss.iss_telemetry.eclipsed}")
print(f"ISS Geocentric Lat: {iss.iss_telemetry.sublat}")
print(f"ISS Geocentric Lon: {iss.iss_telemetry.sublong}")
print(f"ISS Elevation: {iss.iss_telemetry.elevation} Meters")
print(f"ISS Elevation: {meters_to_miles(iss.iss_telemetry.elevation)} Miles")

# Get ISS Next Passes
# station = ephem.Observer() (default is intilized observer)
# start = start date/time (default is self.obs.date)
# satellite = tle data (default is self.iss_telemetry)
# duration = number of days to show visiby passes for (Default: 5)
iss_next_passes = iss.iss_passes(duration=3)

# ISS pass start and end time (times in UTC)
#print("ISS Passes (Times UTC)")
#for i in iss_next_passes:
#    print(i['eclipsed'], i['aos'], i['los'])

print("Visible (eclipsed=False) ISS passes converted to local time")
for i in iss_next_passes:
    if not i['eclipsed']: 
       print(i['eclipsed'], to_local(i['aos']), to_local(i['los']) , math.degrees(i['alt_max']))
   

