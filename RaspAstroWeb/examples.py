# Examples using the RaspAstro classes
# AstroData (Moon, Sun, More to Come...) from ephem
from raspastroinfo import AstroData
# ISSData (ISS telemerty and pass information) using ephem
from raspissinfo import ISSData
from config import *

from datetime import datetime
from dateutil import tz
import math
import time
from rasp_calc_func import *

#MY_LAT = "36:43:41.538" # Your latitude in DMS
#MY_LON = "-76:35:0.8232" # Your longitude in DMS

print("=====================================")
print("AstroData Examples")
print("=====================================")

# Intialize AstroData 
# Optional Keyword args:
# obslat = Observer Latitude in DMS (Default: 36:43:41.538)
# obslon = Observers Longitude in DMS (Default: -76:35:0.8232)
# obsepoch = Observation Time in UTC (Default: datetime.utcnow()))
# obselev = Observers Elevation (Default: 3) (meters)
astro = AstroData(obslat=MY_LAT, obslon=MY_LON)
print(f"Observer Date (Local time): {to_local(astro.obs.date.datetime())}")

print("========Moon Info========")
# Get Moon Info
astro.moon_info()
for key in astro.moon_data:
    print(f"{key} = {astro.moon_data[key]}")

print("========Sun Info========")
# Get Sun Info
sun = astro.sun_info()
for key in astro.sun_data:
    print(f"{key} = {astro.sun_data[key]}")

print(f"Next Sunset (Local time): {to_local(astro.sun_data['next_sunset'].datetime())}")
print(f"Next Sunrise (Local time): {to_local(astro.sun_data['next_sunrise'].datetime())}")

print(f"Next Sun Transit: {astro.sun_data['next_sun_transit']}")


print("=====================================")
print("ISSData Examples")
print("=====================================")

# Initialize ISSData 
# Optional Keyword args:
# obslat = Observer Latitude in DMS(Default: 36:43:41.538)
# obslon = Observers Longitude in DMS(Default: -76:35:0.8232)
# obsepoch = Observation Time in UTC (Default: datetime.utcnow()))
# obselev = Observers Elevation (Default: 3) (meters)
iss = ISSData(obslat=MY_LAT, obslon=MY_LON)
print("========ISS Observer Info========")
print(f"Observers date in local time: {to_local(iss.obs.date.datetime())}")
print(f"Observer lat: {iss.obs.lat}")
print(f"Observer lon: {iss.obs.lon}")
print(f"Observer horizon: {iss.obs.horizon}")
print(f"Satellite: {iss.iss_module_name}")
print(f"tle1: {iss.iss_tle1}")
print(f"tle2: {iss.iss_tle2}")

print("========Current ISS Info========")
print(f"ISS Eclipsed: {iss.iss_telemetry.eclipsed}")
print(f"ISS Geocentric Lat: {iss.iss_telemetry.sublat}")
print(f"ISS Geocentric Lon: {iss.iss_telemetry.sublong}")
print(f"ISS Elevation: {iss.iss_telemetry.elevation} Meters")
print(f"ISS Elevation: {meters_to_miles(iss.iss_telemetry.elevation)} Miles")

print("========ISS Passes========")
# station = observer info (default is self.obs.copy())
# start = start date/time (default is self.obs.date)
# satellite = tle data (default is self.iss_telemetry)
# sat_name = satellite name (default is self.iss_module_name)
# sat_tle1 = tle1 data line (default is self.iss_tle1)
# sat_tle2 = tle2 data line (default is self.iss_tle2)
# duration = number of days to show passes for (Default: 5)
iss.iss_passes(duration=3)

# ISS pass start and end time (times in UTC)
#print("ISS Passes (Times UTC)")
#for i in iss.iss_next_passes:
#    print(i['eclipsed'], i['aos'], i['los'])

print("Visible (eclipsed=False) and (sun_alt < 0) ISS passes") 
print("Time is converted to local time")
for i in iss.iss_next_passes:
    if not i['eclipsed'] and i['sun_alt'] < 0: 
       print(i['sun_alt'], i['eclipsed'], to_local(i['aos'].datetime()), to_local(i['los'].datetime()) , math.degrees(i['alt_max']), i['constellation'])
   

print("=========Object Info===========")
object = "M31|NGC 224|UGC 454|MCG 7-2-16|ZWG 535.17|PGC2557 N,f|G|Sb,0:42:44.3,41:16:8,3.5,2000,11346|3702|35"

astro.object_info(catalog=object)
for key in astro.object_data:
    print(f"{key} = {astro.object_data[key]}")

