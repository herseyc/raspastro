import ephem
import math
from datetime import datetime

class AstroData():
   
    def __init__(self, **kw):
        obslat = 36.779397335
        obslon = -76.535577396
        # Setup Observer
        self.obs = ephem.Observer()
        self.obs.lon = obslon
        self.obs.lat = obslat
        self.obs.date = datetime.utcnow()


    def suninfo(self):
        sun = ephem.Sun()
        sun.compute(self.obs)
        sun_data = {}

        sun_data['astronomical_twilight_starts'] = ephem.localtime(self.obs.next_setting(sun)).ctime()
        sun_data['astronomical_twilight_ends'] = ephem.localtime(self.obs.next_rising(sun)).ctime()
         
        return sun_data


    def mooninfo(self):
        sun = ephem.Sun()
        sun.compute(self.obs)
        moon = ephem.Moon()
        moon.compute(self.obs)
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

        moon_data['next_new_moon'] = ephem.localtime(ephem.next_new_moon(self.obs.date)).ctime()
        moon_data['next_full_moon'] = ephem.localtime(ephem.next_full_moon(self.obs.date)).ctime()

        return moon_data
       





