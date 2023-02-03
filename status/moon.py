import ephem
import math
from datetime import datetime

moon_data = {}

def mooninfo():

    obs = ephem.Observer()
    # TODO Get Location from GPS
    obs.lon = -76.535577396
    obs.lat = 36.779397335
    obs.date = datetime.utcnow()


    sun = ephem.Sun()
    sun.compute(obs)

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


    if moon_data["moon_phase_percent"] >= 0 and moon_data["moon_phase_percent"] < 15:
        moon_data['moon_phase_sign'] = '🌕'
        moon_data['moon_phase_name'] = 'New Moon'

    elif moon_data["moon_phase_percent"] >= 15 and moon_data["moon_phase_percent"] < 35:
        moon_data['moon_phase_sign'] = '🌔'
        moon_data['moon_phase_name'] = 'Crescent'

    elif moon_data["moon_phase_percent"] >= 35 and moon_data["moon_phase_percent"] < 65 and moon_date['moon_phase'] == 'Waxing':
        moon_data['moon_phase_sign'] = '🌓'
        moon_data['moon_phase_name'] = 'First Quarter'

    elif moon_data["moon_phase_percent"] >= 35 and moon_data["moon_phase_percent"] < 65 and moon_date['moon_phase'] == 'Waning':
        moon_data['moon_phase_sign'] = '🌓'
        moon_data['moon_phase_name'] = 'Last Quarter'

    elif moon_data["moon_phase_percent"] >= 65 and moon_data["moon_phase_percent"] < 85:
        moon_data['moon_phase_sign'] = '🌒'
        moon_data['moon_phase_name'] = 'Gibbous'

    elif moon_data["moon_phase_percent"] >= 85 and moon_data["moon_phase_percent"] <= 100:
        moon_data['moon_phase_sign'] = '🌑'
        moon_data['moon_phase_name'] = 'Full Moon'


    for key in moon_data:
        print(f"{key} = {moon_data[key]}")

mooninfo()
#print(f"Percent Illuminated: {round(moon_data['moon_phase_percent'])}%")





