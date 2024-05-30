########################################################
# raspastroinfo.py
# AstroData Class
# Create lists of Sun and Moon info using ephem
#
# Visit my EAA site: http://www.suffolksky.com/
########################################################
import ephem
import math
import numpy
import socket
from datetime import datetime

class AstroData:
    '''
    AStroData Class - Set up observer, get sun_info, moon_info,
    and planet_info. All times are in UTC time. 
    '''
   
    def __init__(self, **kw):
        ''' Initialize Observer Data '''
        obslat = kw.get("obslat", "36:43:41.538")
        obslon = kw.get("obslon", "-76:35:0.8232")
        obsepoch = kw.get("obsepoch", datetime.utcnow())
        obselev = kw.get("obslev", 3)
        obshorizon = kw.get("obshorizon", "0:34:0")
        obspressure = kw.get("obspressure", 0)
        obstemp = kw.get("obstemp", 0)
        # Setup Observer
        self.obs = ephem.Observer()
        self.obs.lon = obslon
        self.obs.lat = obslat
        self.obs.elev = obselev
        self.obs.horizon = obshorizon
        self.obs.date = obsepoch
        self.obs.pressure = obspressure
        self.obs.temperature = obstemp
        self.sidereal = self.obs.sidereal_time()
        # Initilize list to hold dictionary of catalogobjects
        self.catalog_objects_data = []


    def sun_info(self, **kw):
        ''' 
        Sun Information - creates sun_data dictionary with Sun information
        Dictionary also includes some Earth information (hlon, hlat, radius).
        '''
        obs = kw.get("obs", self.obs)
        sun = ephem.Sun()
        sun.compute(obs)
        self.sun_data = {}
        sun_alt = round(math.degrees(sun.alt), 1)

        # All times are in UTC Time
        self.sun_data['next_sunset'] = self.obs.next_setting(sun, use_center=True)
        self.sun_data['next_sunrise'] = self.obs.next_rising(sun, use_center=True)
        self.sun_data['previous_solstice'] = ephem.previous_solstice(obs.date)
        self.sun_data['previous_equinox'] = ephem.previous_equinox(obs.date)
        self.sun_data['next_solstice'] = ephem.next_solstice(obs.date)
        self.sun_data['next_equinox'] = ephem.next_equinox(obs.date)
        self.sun_data['sun_alt'] = sun_alt
        self.sun_data['earth_hlon'] = sun.hlon
        self.sun_data['earth_hlat'] = sun.hlat
        self.sun_data['earth_radius'] = ephem.earth_radius
        self.sun_data['sun_radius'] = ephem.sun_radius
        self.sun_data['next_sun_transit'] = self.obs.next_transit(sun)
         

    def moon_info(self, **kw):
        ''' 
        Moon Information - creates moon_data dictionary with Moon info
        '''
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

        # All times in UTC Time
        self.moon_data['next_new_moon'] = ephem.next_new_moon(self.obs.date)
        self.moon_data['next_full_moon'] = ephem.next_full_moon(self.obs.date)
        self.moon_data['next_moon_transit'] = self.obs.next_transit(moon)
        self.moon_data['constellation'] = ephem.constellation(moon)
        self.moon_data['hlat'] = moon.hlat
        self.moon_data['hlon'] = moon.hlon
        self.moon_data['next_moonset'] = self.obs.next_setting(moon)
        self.moon_data['next_moonrise'] = self.obs.next_rising(moon)

       
    def planet_info(self, **kw):
        ''' 
        Planet Information - Creates a dictionary for each planet with
        the planets info. Mercury, Venus, Mars, Jupiter, Saturn, Uranus,
        and Neptune.
        '''
        obs = kw.get("obs", self.obs)
        # Mercury
        self.mercury = {}
        c_mercury = ephem.Mercury()
        c_mercury.compute(obs)
        self.mercury['name'] =  c_mercury.name
        self.mercury['hlat'] =  c_mercury.hlat
        self.mercury['hlon'] =  c_mercury.hlon
        self.mercury['elong'] =  c_mercury.elong
        self.mercury['mag'] =  c_mercury.mag
        self.mercury['radius'] =  c_mercury.radius
        self.mercury['a_ra'] =  c_mercury.a_ra
        self.mercury['a_dec'] =  c_mercury.a_dec
        self.mercury['alt'] =  round(math.degrees(c_mercury.alt), 1)
        self.mercury['az'] =  round(math.degrees(c_mercury.az), 1)
        self.mercury['sun_distance'] =  round(c_mercury.sun_distance, 4)
        self.mercury['earth_distance'] =  round(c_mercury.earth_distance, 4)
        self.mercury['constellation'] =  ephem.constellation(c_mercury)
        self.mercury['next_transit'] = obs.next_transit(c_mercury) 
      
        # Venus
        self.venus = {}
        c_venus = ephem.Venus()
        c_venus.compute(obs)
        self.venus['name'] =  c_venus.name
        self.venus['hlat'] =  c_venus.hlat
        self.venus['hlon'] =  c_venus.hlon
        self.venus['elong'] =  c_venus.elong
        self.venus['mag'] =  c_venus.mag
        self.venus['radius'] =  c_venus.radius
        self.venus['a_ra'] =  c_venus.a_ra
        self.venus['a_dec'] =  c_venus.a_dec
        self.venus['alt'] =  round(math.degrees(c_venus.alt), 1)
        self.venus['az'] =  round(math.degrees(c_venus.az), 1)
        self.venus['sun_distance'] =  round(c_venus.sun_distance, 4)
        self.venus['earth_distance'] =  round(c_venus.earth_distance, 4)
        self.venus['constellation'] =  ephem.constellation(c_venus)
        self.venus['next_transit'] = obs.next_transit(c_venus) 
   
        # Mars
        self.mars = {}
        c_mars = ephem.Mars()
        c_mars.compute(obs)
        self.mars['name'] =  c_mars.name
        self.mars['hlat'] =  c_mars.hlat
        self.mars['hlon'] =  c_mars.hlon
        self.mars['elong'] =  c_mars.elong
        self.mars['mag'] =  c_mars.mag
        self.mars['radius'] =  c_mars.radius
        self.mars['a_ra'] =  c_mars.a_ra
        self.mars['a_dec'] =  c_mars.a_dec
        self.mars['alt'] =  round(math.degrees(c_mars.alt), 1)
        self.mars['az'] =  round(math.degrees(c_mars.az), 1)
        self.mars['sun_distance'] =  round(c_mars.sun_distance, 4)
        self.mars['earth_distance'] =  round(c_mars.earth_distance, 4)
        self.mars['constellation'] =  ephem.constellation(c_mars)
        self.mars['next_transit'] = obs.next_transit(c_mars) 

        # Jupiter
        self.jupiter = {}
        c_jupiter = ephem.Jupiter()
        c_jupiter.compute(obs)
        self.jupiter['name'] =  c_jupiter.name
        self.jupiter['hlat'] =  c_jupiter.hlat
        self.jupiter['hlon'] =  c_jupiter.hlon
        self.jupiter['elong'] =  c_jupiter.elong
        self.jupiter['mag'] =  c_jupiter.mag
        self.jupiter['radius'] =  c_jupiter.radius
        self.jupiter['a_ra'] =  c_jupiter.a_ra
        self.jupiter['a_dec'] =  c_jupiter.a_dec
        self.jupiter['alt'] =  round(math.degrees(c_jupiter.alt), 1)
        self.jupiter['az'] =  round(math.degrees(c_jupiter.az), 1)
        self.jupiter['sun_distance'] =  round(c_jupiter.sun_distance, 4)
        self.jupiter['earth_distance'] =  round(c_jupiter.earth_distance, 4)
        self.jupiter['constellation'] =  ephem.constellation(c_jupiter)
        self.jupiter['next_transit'] = obs.next_transit(c_jupiter) 

        # Saturn
        self.saturn = {}
        c_saturn = ephem.Saturn()
        c_saturn.compute(obs)
        self.saturn['name'] =  c_saturn.name
        self.saturn['hlat'] =  c_saturn.hlat
        self.saturn['hlon'] =  c_saturn.hlon
        self.saturn['elong'] =  c_saturn.elong
        self.saturn['mag'] =  c_saturn.mag
        self.saturn['radius'] =  c_saturn.radius
        self.saturn['a_ra'] =  c_saturn.a_ra
        self.saturn['a_dec'] =  c_saturn.a_dec
        self.saturn['alt'] =  round(math.degrees(c_saturn.alt), 1)
        self.saturn['az'] =  round(math.degrees(c_saturn.az), 1)
        self.saturn['sun_distance'] =  round(c_saturn.sun_distance, 4)
        self.saturn['earth_distance'] =  round(c_saturn.earth_distance, 4)
        self.saturn['constellation'] =  ephem.constellation(c_saturn)
        self.saturn['next_transit'] = obs.next_transit(c_saturn) 

        # Uranus
        self.uranus = {}
        c_uranus = ephem.Uranus()
        c_uranus.compute(obs)
        self.uranus['name'] =  c_uranus.name
        self.uranus['hlat'] =  c_uranus.hlat
        self.uranus['hlon'] =  c_uranus.hlon
        self.uranus['elong'] =  c_uranus.elong
        self.uranus['mag'] =  c_uranus.mag
        self.uranus['radius'] =  c_uranus.radius
        self.uranus['a_ra'] =  c_uranus.a_ra
        self.uranus['a_dec'] =  c_uranus.a_dec
        self.uranus['alt'] =  round(math.degrees(c_uranus.alt), 1)
        self.uranus['az'] =  round(math.degrees(c_uranus.az), 1)
        self.uranus['sun_distance'] =  round(c_uranus.sun_distance, 4)
        self.uranus['earth_distance'] =  round(c_uranus.earth_distance, 4)
        self.uranus['constellation'] =  ephem.constellation(c_uranus)
        self.uranus['next_transit'] = obs.next_transit(c_uranus) 

        # Neptune
        self.neptune = {}
        c_neptune = ephem.Neptune()
        c_neptune.compute(obs)
        self.neptune['name'] =  c_neptune.name
        self.neptune['hlat'] =  c_neptune.hlat
        self.neptune['hlon'] =  c_neptune.hlon
        self.neptune['elong'] =  c_neptune.elong
        self.neptune['mag'] =  c_neptune.mag
        self.neptune['radius'] =  c_neptune.radius
        self.neptune['a_ra'] =  c_neptune.a_ra
        self.neptune['a_dec'] =  c_neptune.a_dec
        self.neptune['alt'] =  round(math.degrees(c_neptune.alt), 1)
        self.neptune['az'] =  round(math.degrees(c_neptune.az), 1)
        self.neptune['sun_distance'] =  round(c_neptune.sun_distance, 4)
        self.neptune['earth_distance'] =  round(c_neptune.earth_distance, 4)
        self.neptune['constellation'] =  ephem.constellation(c_neptune)
        self.neptune['next_transit'] = obs.next_transit(c_neptune) 

    def polaris_info(self, **kw):
        ''' Polaris Information '''
        obs = kw.get("obs", self.obs)
        self.polaris_data = {} 
        self.polaris = ephem.star("Polaris")
        self.polaris.compute(obs)
        # Compute polar scope rectile location for Polaris
        j2000 = ephem.Date('2000/01/01 12:00:00')
        d = obs.date - j2000
        utstr = obs.date.datetime().strftime("%H:%M:%S")
        ut = float(utstr.split(":")[0]) + float(utstr.split(":")[1])/60 + float(utstr.split(":")[2])/3600
        lon = numpy.rad2deg(float(repr(obs.lon)))
        lst = 100.46 + 0.985647 * d + lon + 15 * ut
        lst = lst - int(lst / 360) * 360

        phourangle = lst - numpy.rad2deg(float(repr(self.polaris.ra)))
        if phourangle < 0:
            phourangle += 360
        elif phourangle > 360:
            phourangle -= 360

        self.polaris_data['phourangle'] = phourangle
        self.polaris_data['from_pole'] = ephem.degrees(ephem.degrees('90') - self.polaris.a_dec)
        self.polaris_data['next_transit'] = obs.next_transit(self.polaris)
        
    def object_info(self, **kw):
        '''
        Takes XEphem formated ecatalog data and computes object information
        '''
        obs = kw.get("obs", self.obs)
        catalog = kw.get("catalog", "None")
        self.object_data = {}
        # Use ephem.readdb(line)
        # Add dictionary of catalog object data to catalogobject list
        if catalog == "None":
            self.object_data.append["No catalog data provided"]
            return

        xephem_edb_objecttypes = {
                "A": "Cluster of galaxies",
                "B": "Star, binary",
                "C": "Cluster, globular",
                "D": "Star, visual double",
                "F": "Nebula, diffuse",
                "G": "Galaxy, spiral",
                "H": "Galaxy, spherical",
                "J": "Radio",
                "K": "Nebula, dark",
                "L": "Pulsar",
                "M": "Star, multiple",
                "N": "Nebula, bright",
                "O": "Cluster, open",
                "P": "Nebula, planetary",
                "Q": "Quasar",
                "R": "Supernova remnant",
                "S": "Star",
                "T": "Stellar object",
                "U": "Cluster, with nebulosity",
                "Y": "Supernova",
                "V": "Star, variable",
            }

        object = ephem.readdb(catalog)
        object.compute(obs)
        self.object_data['name'] = object.name

        if isinstance(object, ephem.FixedBody):
            self.object_data['class'] = object._class
            self.object_data['class_name'] = xephem_edb_objecttypes[object._class]
            self.object_data['perihelion_epoch'] = "NA"
        elif isinstance(object, ephem.EllipticalBody):
            self.object_data['class'] = "Elliptical"
            self.object_data['class_name'] = "Elliptical"
            self.object_data['perihelion_epoch'] = "NA"
        elif isinstance(object, ephem.HyperbolicBody):
            self.object_data['class'] = "Hyperbolic"
            self.object_data['class_name'] = "Hyperbolic"
            self.object_data['perihelion_epoch'] = object._epoch_p
        elif isinstance(object, ephem.ParabolicBody):
            self.object_data['class'] = "Parabolic"
            self.object_data['class_name'] = "Parabolic"
            self.object_data['perihelion_epoch'] = object._epoch_p
        else:
            self.object_data['class'] = "NA"
            self.object_data['class_name'] = "NA"
            self.object_data['perihelion_epoch'] = "NA"

        self.object_data['a_ra'] = object.a_ra
        self.object_data['a_dec'] = object.a_dec
        self.object_data['mag'] = object.mag
        self.object_data['size'] = object.size
        self.object_data['alt'] = object.alt
        self.object_data['az'] = object.az
        self.object_data['circumpolar'] = object.circumpolar
        self.object_data['constellation'] = ephem.constellation(object)

        if object.circumpolar:
            self.object_data['next_rising'] = datetime.utcnow
            self.object_data['next_setting'] = datetime.utcnow
        else:      
            self.object_data['next_rising'] = obs.next_rising(object)
            self.object_data['next_setting'] = obs.next_setting(object)

        self.object_data['next_transit'] = obs.next_transit(object)

