import ephem
import math
from datetime import datetime

# Tinkering with ephem module to get data about the moon.

moon_data = {}

def mooninfo():

    obs = ephem.Observer()
    # TODO Get Location from GPS
    obs.lon = -76.535577396
    obs.lat = 36.779397335
    obs.date = datetime.utcnow()

    sun = ephem.Sun()
    sun.compute(obs)

    moon_data['astronomical_twilight_starts'] = ephem.localtime(obs.next_setting(sun)).ctime()
    moon_data['astronomical_twilight_ends'] = ephem.localtime(obs.next_rising(sun)).ctime()


    moon = ephem.Moon()
    moon.compute(obs)

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

    moon_data['next_new_moon'] = ephem.localtime(ephem.next_new_moon(obs.date)).ctime()
    moon_data['next_full_moon'] = ephem.localtime(ephem.next_full_moon(obs.date)).ctime()

    return moon_data


moon_information = mooninfo()

print(moon_information)



