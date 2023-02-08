########################################################
# raspastroinfo.py
# AstroData Class
# Create lists of Sun and Moon info using ephem
#
# Visit my EAA site: http://www.suffolksky.com/
########################################################
import ephem
import math
from datetime import datetime

class AstroData():
   
    def __init__(self, **kw):
        ''' Initialize Observer Data '''
        obslat = kw.get("obslat", "36:43:41.538")
        obslon = kw.get("obslon", "-76:35:0.8232")
        obsepoch = kw.get("obsepoch", datetime.utcnow())
        obselev = kw.get("obslev", 3)
        obshorizon = kw.get("obshorizon", "0:34")
        # Setup Observer
        self.obs = ephem.Observer()
        self.obs.lon = obslon
        self.obs.lat = obslat
        self.obs.elev = obselev
        self.obs.horizon = obshorizon
        self.obs.date = datetime.utcnow()


    def sun_info(self, **kw):
        ''' Sun Information '''
        obs = kw.get("obs", self.obs)
        sun = ephem.Sun()
        sun.compute(obs)
        sun_data = {}

        # UTC Time
        next_twilight_starts = self.obs.next_setting(sun)
        next_twilight_ends = self.obs.next_rising(sun)
        sun_data['astronomical_twilight_starts'] = self.obs.next_setting(sun)
        sun_data['astronomical_twilight_ends'] = self.obs.next_rising(sun)
        sun_data['previous_solstice'] = ephem.previous_solstice(obs.date)
        sun_data['previous_equinox'] = ephem.previous_equinox(obs.date)
        sun_data['next_solstice'] = ephem.next_solstice(obs.date)
        sun_data['next_equinox'] = ephem.next_equinox(obs.date)
         
        return sun_data


    def moon_info(self, **kw):
        ''' Moon Information '''
        obs = kw.get("obs", self.obs)
        sun = ephem.Sun()
        sun.compute(obs)
        moon = ephem.Moon()
        moon.compute(obs)
        moon_data = {}

        #Determine Moon %Illuminated Phase
        moon_phase_percent = round(moon.moon_phase * 100)
        moon_data["moon_phase_percent"] = moon_phase_percent 

        sun_lon = ephem.Ecliptic(sun).lon
        moon_lon = ephem.Ecliptic(moon).lon
        sm_angle = (moon_lon - sun_lon) % math.tau
        moon_quarter = int(sm_angle * 4.0 // math.tau)

        # Determine if Moon is Waxing or Waning
        if moon_quarter < 2:
            moon_data['moon_quarter'] = 'Waxing'
        else:
            moon_data['moon_quarter'] = 'Waning'

        # Current percentage of 29.53 day Lunar cycle. 
        cycle_percent = round((sm_angle / math.tau) * 100, 2)
        moon_data['cycle_percent'] = cycle_percent

        if cycle_percent <= 50:
            # waxing
            if moon_phase_percent >= 0 and moon_phase_percent < 15:
                moon_data['moon_phase_emoji'] = '🌑'
                moon_data['moon_phase_name'] = 'New Moon'
            elif moon_phase_percent >= 15 and moon_phase_percent < 35:
                moon_data['moon_phase_emoji'] = '🌒'
                moon_data['moon_phase_name'] = 'Crescent'
            elif moon_phase_percent >= 35 and moon_phase_percent < 65:
                moon_data['moon_phase_emoji'] = '🌓'
                moon_data['moon_phase_name'] = 'First Quarter'
            elif moon_phase_percent >= 65 and moon_phase_percent < 85:
                moon_data['moon_phase_emoji'] = '🌔'
                moon_data['moon_phase_name'] = 'Gibbous'
            elif moon_phase_percent >= 85 and moon_phase_percent <= 100:
                moon_data['moon_phase_emoji'] = '🌕'
                moon_data['moon_phase_name'] = 'Full Moon'
        else:
            # waning
            if moon_phase_percent >= 85 and moon_phase_percent <= 100:
                moon_data['moon_phase_emoji'] = '🌕'
                moon_data['moon_phase_name'] = 'Full Moon'
            elif moon_phase_percent >= 65 and moon_phase_percent < 85:
                moon_data['moon_phase_emoji'] = '🌖'
                moon_data['moon_phase_name'] = 'Gibbous'
            elif moon_phase_percent >= 35 and moon_phase_percent < 65:
                moon_data['moon_phase_emoji'] = '🌗'
                moon_data['moon_phase_name'] = 'Last Quarter'
            elif moon_phase_percent >= 15 and moon_phase_percent < 35:
                moon_data['moon_phase_emoji'] = '🌘'
                moon_data['moon_phase_name'] = 'Crescent'
            elif moon_phase_percent >= 0 and moon_phase_percent < 15:
                moon_data['moon_phase_emoji'] = '🌑'
                moon_data['moon_phase_name'] = 'New Moon'

        # UTC Time
        moon_data['next_new_moon'] = ephem.next_new_moon(self.obs.date)
        moon_data['next_full_moon'] = ephem.next_full_moon(self.obs.date)

        return moon_data
       





