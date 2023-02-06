from urllib import request
import datetime as dt
import ephem
import math
import predict

degrees_per_radian = 180.0 / math.pi

# Look here for hints on predicting ISS passes
# https://stackoverflow.com/questions/52591629/pyephem-and-pypredict-gpredict-differences
def passes(station, satellite, start=None, duration=7):
    result = []
    if start is not None:
        station.date = ephem.date(start)
    end = ephem.date(station.date + duration)
    while station.date < end:
        t_aos, azr, t_max, elt, t_los, azs = station.next_pass(satellite)
        result.append({'aos': t_aos.datetime(), 'los': t_los.datetime()})
        station.date = t_los + ephem.second
    return result


obslat = 36.779397335
obslon = -76.535577396
obs = ephem.Observer()
obs.lon = obslon
obs.lat = obslat
obs.elev = 0
obs.date = dt.datetime.utcnow()

print(f"Date: {dt.datetime.utcnow()}")

# Get ISS Data from Celestrak.org
iss_tledata = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544"
f = request.urlopen(iss_tledata)
iss = f.readlines()

# Format data so we can pass it to ephem
tle = []
for sub in iss:
    fix = str(sub)
    fix = fix.split("'")[1].split("'")[0] 
    fix = fix.replace("\\n", "")
    fix = fix.replace("\\r", "")
    fix = fix.strip()
    tle.append(fix)

# tle data for ephem
iss_module_name = tle[0]
iss_tle1 = tle[1]
iss_tle2 = tle[2]

iss_telemetry = ephem.readtle(iss_module_name, iss_tle1, iss_tle2)
iss_telemetry.compute(obs)

epoch = dt.datetime.utcnow()
for i in passes(obs, iss_telemetry, epoch, 5):
    print(i['aos'], i['los'])


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

print("exit")
