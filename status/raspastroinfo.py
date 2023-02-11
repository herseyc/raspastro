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

class AstroData:
   
    def __init__(self, **kw):
        ''' Initialize Observer Data '''
        obslat = kw.get("obslat", "36:43:41.538")
        obslon = kw.get("obslon", "-76:35:0.8232")
        obsepoch = kw.get("obsepoch", datetime.utcnow())
        obselev = kw.get("obslev", 3)
        obshorizon = kw.get("obshorizon", "5:34")
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
        self.sun_data = {}
        sun_alt = round(math.degrees(sun.alt), 1)

        # UTC Time
        self.sun_data['next_sunset'] = self.obs.next_setting(sun)
        self.sun_data['next_sunrise'] = self.obs.next_rising(sun)
        self.sun_data['previous_solstice'] = ephem.previous_solstice(obs.date)
        self.sun_data['previous_equinox'] = ephem.previous_equinox(obs.date)
        self.sun_data['next_solstice'] = ephem.next_solstice(obs.date)
        self.sun_data['next_equinox'] = ephem.next_equinox(obs.date)
        self.sun_data['sun_alt'] = sun_alt
         

    def moon_info(self, **kw):
        ''' Moon Information '''
        obs = kw.get("obs", self.obs)
        sun = ephem.Sun()
        sun.compute(obs)
        moon = ephem.Moon()
        moon.compute(obs)
        self.moon_data = {}

        #Determine Moon %Illuminated Phase
        moon_phase_percent = round(moon.moon_phase * 100)
        self.moon_data["moon_phase_percent"] = moon_phase_percent 

        self.moon_data["moon_alt"] = round(math.degrees(moon.alt), 1) 

        sun_lon = ephem.Ecliptic(sun).lon
        moon_lon = ephem.Ecliptic(moon).lon
        sm_angle = (moon_lon - sun_lon) % math.tau
        moon_quarter = int(sm_angle * 4.0 // math.tau)

        # Determine if Moon is Waxing or Waning
        if moon_quarter < 2:
            self.moon_data['moon_quarter'] = 'Waxing'
        else:
            self.moon_data['moon_quarter'] = 'Waning'

        # Current percentage of 29.53 day Lunar cycle. 
        cycle_percent = round((sm_angle / math.tau) * 100, 2)
        self.moon_data['cycle_percent'] = cycle_percent

        if cycle_percent <= 50:
            # waxing
            if moon_phase_percent >= 0 and moon_phase_percent < 15:
                self.moon_data['moon_phase_emoji'] = '🌑'
                self.moon_data['moon_phase_name'] = 'New Moon'
            elif moon_phase_percent >= 15 and moon_phase_percent < 35:
                self.moon_data['moon_phase_emoji'] = '🌒'
                self.moon_data['moon_phase_name'] = 'Crescent'
            elif moon_phase_percent >= 35 and moon_phase_percent < 65:
                self.moon_data['moon_phase_emoji'] = '🌓'
                self.moon_data['moon_phase_name'] = 'First Quarter'
            elif moon_phase_percent >= 65 and moon_phase_percent < 85:
                self.moon_data['moon_phase_emoji'] = '🌔'
                self.moon_data['moon_phase_name'] = 'Gibbous'
            elif moon_phase_percent >= 85 and moon_phase_percent <= 100:
                self.moon_data['moon_phase_emoji'] = '🌕'
                self.moon_data['moon_phase_name'] = 'Full Moon'
        else:
            # waning
            if moon_phase_percent >= 85 and moon_phase_percent <= 100:
                self.moon_data['moon_phase_emoji'] = '🌕'
                self.moon_data['moon_phase_name'] = 'Full Moon'
            elif moon_phase_percent >= 65 and moon_phase_percent < 85:
                self.moon_data['moon_phase_emoji'] = '🌖'
                self.moon_data['moon_phase_name'] = 'Gibbous'
            elif moon_phase_percent >= 35 and moon_phase_percent < 65:
                self.moon_data['moon_phase_emoji'] = '🌗'
                self.moon_data['moon_phase_name'] = 'Last Quarter'
            elif moon_phase_percent >= 15 and moon_phase_percent < 35:
                self.moon_data['moon_phase_emoji'] = '🌘'
                self.moon_data['moon_phase_name'] = 'Crescent'
            elif moon_phase_percent >= 0 and moon_phase_percent < 15:
                self.moon_data['moon_phase_emoji'] = '🌑'
                self.moon_data['moon_phase_name'] = 'New Moon'

        # UTC Time
        self.moon_data['next_new_moon'] = ephem.next_new_moon(self.obs.date)
        self.moon_data['next_full_moon'] = ephem.next_full_moon(self.obs.date)

       
    def planet_info(self, **kw):
        ''' Moon Information '''
        obs = kw.get("obs", self.obs)
        # Mercury
        self.mercury = {}
        c_mercury = ephem.Mercury()
        c_mercury.compute(obs)
        self.mercury['name'] =  c_mercury.name
        self.mercury['hlat'] =  c_mercury.hlat
        self.mercury['hlon'] =  c_mercury.hlon
        self.mercury['mag'] =  c_mercury.mag
        self.mercury['alt'] =  round(math.degrees(c_mercury.alt), 1)
        self.mercury['sun_distance'] =  round(c_mercury.sun_distance, 4)
        self.mercury['earth_distance'] =  round(c_mercury.earth_distance, 4)
      
        # Venus
        self.venus = {}
        c_venus = ephem.Venus()
        c_venus.compute(obs)
        self.venus['name'] =  c_venus.name
        self.venus['hlat'] =  c_venus.hlat
        self.venus['hlon'] =  c_venus.hlon
        self.venus['mag'] =  c_venus.mag
        self.venus['alt'] =  round(math.degrees(c_venus.alt), 1)
        self.venus['sun_distance'] =  round(c_venus.sun_distance, 4)
        self.venus['earth_distance'] =  round(c_venus.earth_distance, 4)
   
        # Mars
        self.mars = {}
        c_mars = ephem.Mars()
        c_mars.compute(obs)
        self.mars['name'] =  c_mars.name
        self.mars['hlat'] =  c_mars.hlat
        self.mars['hlon'] =  c_mars.hlon
        self.mars['mag'] =  c_mars.mag
        self.mars['alt'] =  round(math.degrees(c_mars.alt), 1)
        self.mars['sun_distance'] =  round(c_mars.sun_distance, 4)
        self.mars['earth_distance'] =  round(c_mars.earth_distance, 4)

        # Jupiter
        self.jupiter = {}
        c_jupiter = ephem.Jupiter()
        c_jupiter.compute(obs)
        self.jupiter['name'] =  c_jupiter.name
        self.jupiter['hlat'] =  c_jupiter.hlat
        self.jupiter['hlon'] =  c_jupiter.hlon
        self.jupiter['mag'] =  c_jupiter.mag
        self.jupiter['alt'] =  round(math.degrees(c_jupiter.alt), 1)
        self.jupiter['sun_distance'] =  round(c_jupiter.sun_distance, 4)
        self.jupiter['earth_distance'] =  round(c_jupiter.earth_distance, 4)

        # Saturn
        self.saturn = {}
        c_saturn = ephem.Saturn()
        c_saturn.compute(obs)
        self.saturn['name'] =  c_saturn.name
        self.saturn['hlat'] =  c_saturn.hlat
        self.saturn['hlon'] =  c_saturn.hlon
        self.saturn['mag'] =  c_saturn.mag
        self.saturn['alt'] =  round(math.degrees(c_saturn.alt), 1)
        self.saturn['sun_distance'] =  round(c_saturn.sun_distance, 4)
        self.saturn['earth_distance'] =  round(c_saturn.earth_distance, 4)

        # Uranus
        self.uranus = {}
        c_uranus = ephem.Uranus()
        c_uranus.compute(obs)
        self.uranus['name'] =  c_uranus.name
        self.uranus['hlat'] =  c_uranus.hlat
        self.uranus['hlon'] =  c_uranus.hlon
        self.uranus['mag'] =  c_uranus.mag
        self.uranus['alt'] =  round(math.degrees(c_uranus.alt), 1)
        self.uranus['sun_distance'] =  round(c_uranus.sun_distance, 4)
        self.uranus['earth_distance'] =  round(c_uranus.earth_distance, 4)

        # Neptune
        self.neptune = {}
        c_neptune = ephem.Neptune()
        c_neptune.compute(obs)
        self.neptune['name'] =  c_neptune.name
        self.neptune['hlat'] =  c_neptune.hlat
        self.neptune['hlon'] =  c_neptune.hlon
        self.neptune['mag'] =  c_neptune.mag
        self.neptune['alt'] =  round(math.degrees(c_neptune.alt), 1)
        self.neptune['sun_distance'] =  round(c_neptune.sun_distance, 4)
        self.neptune['earth_distance'] =  round(c_neptune.earth_distance, 4)

