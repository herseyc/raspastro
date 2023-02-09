import ephem
import math
from datetime import datetime
from urllib import request


class ISSData:

    def __init__(self, **kw):
        obslat = kw.get("obslat", "36:43:41.538")
        obslon = kw.get("obslon", "-76:35:0.8232")
        obsepoch = kw.get("obsepoch", datetime.utcnow())
        obselev = kw.get("obslev", 3)
        obshorizon = kw.get("obshorizon", '10:34')
        # Setup Observer
        self.obs = ephem.Observer()
        self.obs.lon = obslon
        self.obs.lat = obslat
        self.obs.date = obsepoch
        self.obs.elev = obselev
        self.obs.horizon = obshorizon
        self.degrees_per_radian = 180.0 / math.pi
        self.iss_tle()


    def iss_tle(self):
        tle_data_file = "isstle.data"
        now_weekday = datetime.now().weekday()
        tle = []
        new_file = False

        try:
            with open(tle_data_file) as tledata:
                data = tledata.readline()
                data_list = data.split("|")
                weekday = int(data_list[0])
        except:
            #Make Weekday Somthing that will not test true
            weekday = datetime.now().weekday() + 6

        # Get tle from celestrak only once per day
        if weekday == now_weekday:
            tle.append(data_list[1])
            tle.append(data_list[2])
            tle.append(data_list[3])
        else: 
            # Get ISS Data from Celestrak.org
            iss_tledata = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544"
            f = request.urlopen(iss_tledata)
            iss = f.readlines()

            # Remove any extra stuff (\n \r ') from tle
            for sub in iss:
                fix = str(sub)
                fix = fix.split("'")[1].split("'")[0]
                fix = fix.replace("\\n", "")
                fix = fix.replace("\\r", "")
                fix = fix.strip()
                tle.append(fix)
            new_file = True

        # Write tle data to tle_data_file
        if new_file:
            with open(tle_data_file, "w") as newtledata:
                newtledata.write(f"{now_weekday}|{tle[0]}|{tle[1]}|{tle[2]}")

        # tle data for ephem
        self.iss_module_name = tle[0]
        self.iss_tle1 = tle[1]
        self.iss_tle2 = tle[2]
     
        self.iss_telemetry = ephem.readtle(self.iss_module_name, self.iss_tle1, self.iss_tle2)
        self.iss_telemetry.compute(self.obs)


    def iss_passes(self, **kw):
        # https://stackoverflow.com/questions/52591629/pyephem-and-pypredict-gpredict-differences
        station = kw.get("station", self.obs.copy())
        start = kw.get("start", self.obs.date) 
        # TODO FIX THIS UP TO TAKE TLE
        sat_name = kw.get("sat_name", self.iss_module_name)
        sat_tle1 = kw.get("sat_tle1", self.iss_tle1)
        sat_tle2 = kw.get("sat_tle2", self.iss_tle2)
        duration = kw.get("duration", 5)
        iss_next_passes = []
        end = ephem.date(station.date + duration)
        sat = ephem.readtle(sat_name, sat_tle1, sat_tle2)
        while station.date < end:
            # Compute iss_telemetry for current station to get eclipsed
            sat.compute(station)
            t_aos, azr, t_max, alt_max, t_los, azs = station.next_pass(sat)
            iss_next_passes.append({'eclipsed': sat.eclipsed, 'aos': t_aos, 'los': t_los, 'azr': azr, 't_max': t_max, 'alt_max': alt_max, 'azs': azs})
            station.date = t_los + ephem.second
       
        return iss_next_passes

