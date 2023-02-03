import ephem
import math
from datetime import datetime

class AstroData():
   
    def __init__(self):
        self.obs = ephem.Observer()
        self.obs.lon = -76.535577396
        self.obs.lat = 36.779397335
        self.obs.date = datetime.utcnow()
        self.sun = ephem.Sun()
        self.sun.compute(self.obs)
        self.moon = ephem.Moon()
        self.moon.compute(self.obs)
        self.astro_data = {}
        self.mooninfo()
        self.suninfo()


    def suninfo(self):
        self.astro_data['astronomical_twilight_starts'] = ephem.localtime(self.obs.next_setting(self.sun)).ctime()
        self.astro_data['astronomical_twilight_ends'] = ephem.localtime(self.obs.next_rising(self.sun)).ctime()
         

    def mooninfo(self):

        #Determine Moon %Illuminated Phase
        moon_phase_percent = round(self.moon.moon_phase * 100)
        self.astro_data["moon_phase_percent"] = moon_phase_percent 

        sun_lon = ephem.Ecliptic(self.sun).lon
        moon_lon = ephem.Ecliptic(self.moon).lon
        sm_angle = (moon_lon - sun_lon) % math.tau
        moon_quarter = int(sm_angle * 4.0 // math.tau)

        # Determine if Moon is Waxing or Waning
        if moon_quarter < 2:
            self.astro_data['moon_quarter'] = 'Waxing'
        else:
            self.astro_data['moon_quarter'] = 'Waning'

        # Current percentage of 29.53 day Lunar cycle. 
        cycle_percent = round((sm_angle / math.tau) * 100, 2)
        self.astro_data['cycle_percent'] = cycle_percent

        if cycle_percent <= 50:
            # waxing
            if moon_phase_percent >= 0 and moon_phase_percent < 15:
                self.astro_data['moon_phase_emoji'] = '🌑'
                self.astro_data['moon_phase_name'] = 'New Moon'
            elif moon_phase_percent >= 15 and moon_phase_percent < 35:
                self.astro_data['moon_phase_emoji'] = '🌒'
                self.astro_data['moon_phase_name'] = 'Crescent'
            elif moon_phase_percent >= 35 and moon_phase_percent < 65:
                self.astro_data['moon_phase_emoji'] = '🌓'
                self.astro_data['moon_phase_name'] = 'First Quarter'
            elif moon_phase_percent >= 65 and moon_phase_percent < 85:
                self.astro_data['moon_phase_emoji'] = '🌔'
                self.astro_data['moon_phase_name'] = 'Gibbous'
            elif moon_phase_percent >= 85 and moon_phase_percent <= 100:
                self.astro_data['moon_phase_emoji'] = '🌕'
                self.astro_data['moon_phase_name'] = 'Full Moon'
        else:
            # waning
            if moon_phase_percent >= 85 and moon_phase_percent <= 100:
                self.astro_data['moon_phase_emoji'] = '🌕'
                self.astro_data['moon_phase_name'] = 'Full Moon'
            elif moon_phase_percent >= 65 and moon_phase_percent < 85:
                self.astro_data['moon_phase_emoji'] = '🌖'
                self.astro_data['moon_phase_name'] = 'Gibbous'
            elif moon_phase_percent >= 35 and moon_phase_percent < 65:
                self.astro_data['moon_phase_emoji'] = '🌗'
                self.astro_data['moon_phase_name'] = 'Last Quarter'
            elif moon_phase_percent >= 15 and moon_phase_percent < 35:
                self.astro_data['moon_phase_emoji'] = '🌘'
                self.astro_data['moon_phase_name'] = 'Crescent'
            elif moon_phase_percent >= 0 and moon_phase_percent < 15:
                self.astro_data['moon_phase_emoji'] = '🌑'
                self.astro_data['moon_phase_name'] = 'New Moon'

        self.astro_data['next_new_moon'] = ephem.localtime(ephem.next_new_moon(self.obs.date)).ctime()
        self.astro_data['next_full_moon'] = ephem.localtime(ephem.next_full_moon(self.obs.date)).ctime()





