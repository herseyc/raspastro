import ephem
import math
from datetime import datetime
from urllib import request



class ISSData():

    def __init__(self, **kw):
        obslat = 36.779397335
        obslon = -76.535577396
        self.obsepoch = datetime.utcnow()
        obselev = 3
        # Setup Observer
        self.obs = ephem.Observer()
        self.obs.lon = obslon
        self.obs.lat = obslat
        self.obs.date = self.obsepoch
        self.obs.elev = obselev
        self.degrees_per_radian = 180.0 / math.pi
        self.iss_tle()


    def iss_tle(self):
        # Get ISS Data from Celestrak.org
        iss_tledata = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544"
        f = request.urlopen(iss_tledata)
        iss = f.readlines()

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
     
        self.iss_telemetry = ephem.readtle(iss_module_name, iss_tle1, iss_tle2)
        self.iss_telemetry.compute(self.obs)


    def iss_passes(self, **kw):
        # https://stackoverflow.com/questions/52591629/pyephem-and-pypredict-gpredict-differences
        station = self.obs
        start = self.obsepoch 
        satellite = self.iss_telemetry
        duration = 5
        iss_next_passes = []
        end = ephem.date(station.date + duration)

        while station.date < end:
            t_aos, azr, t_max, elt, t_los, azs = station.next_pass(satellite)
            iss_next_passes.append({'aos': t_aos.datetime(), 'los': t_los.datetime()})
            station.date = t_los + ephem.second
       
        station.date = self.obsepoch
        return iss_next_passes

