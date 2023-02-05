from urllib import request
import datetime as dt
import ephem
import math

degrees_per_radian = 180.0 / math.pi

# Look here for hints on predicting ISS passes
# https://stackoverflow.com/questions/52591629/pyephem-and-pypredict-gpredict-differences

obslat = 36.779397335
obslon = -76.535577396
obs = ephem.Observer()
obs.lon = obslon
obs.lat = obslat
obs.date = dt.datetime.utcnow()

print(f"Date: {dt.datetime.utcnow()}")

# Get ISS Data from Celestrak.org
iss_tledata = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544"
f = request.urlopen(iss_tledata)
iss = f.readlines()

res = []
for sub in iss:
    fix = str(sub)
    fix = fix.split("'")[1].split("'")[0] 
    fix = fix.replace("\\n", "")
    fix = fix.replace("\\r", "")
    fix = fix.strip()
    res.append(fix)

iss_module_name = res[0]
iss_tle1 = res[1]
iss_tle2 = res[2]

print(iss_module_name)
print(iss_tle1)
print(iss_tle2)

iss_telemetry = ephem.readtle(iss_module_name, iss_tle1, iss_tle2)

iss_telemetry.compute(obs)
iss_range = iss_telemetry.range
iss_alt = iss_telemetry.alt
iss_az = iss_telemetry.az
iss_sublat = iss_telemetry.sublat
iss_sublong = iss_telemetry.sublong
iss_elevation = iss_telemetry.elevation
print(f"ISS Range: {round(iss_range / 1609, 2)} Miles to ISS")
print(f"ISS Alt: {iss_alt * degrees_per_radian}")
print(f"ISS Az: {iss_az * degrees_per_radian}")

print(f"ISS Geocentric Lat: {iss_sublat}")
print(f"ISS Geocentric Lon: {iss_sublong}")
print(f"ISS Elevation: {round(iss_elevation / 1609, 2)} Miles")
print(f"ISS RA: {iss_telemetry.ra}")
print(f"ISS DEC: {iss_telemetry.dec}")

print("Next ISS Pass")
iss_next_pass = obs.next_pass(iss_telemetry)
print(f"Rise Time: {iss_next_pass[0]}")
print(f"Rise Azimuth: {iss_next_pass[1]}")
print(f"Max Altitude Time: {iss_next_pass[2]}")
print(f"Max Altitude: {iss_next_pass[3]}")
print(f"Set Time: {iss_next_pass[4]}")
print(f"Set Azimuth {iss_next_pass[5]}")



