import ephem
import math
from datetime import datetime

moon_data = {}

obs = ephem.Observer()
#Get Location from GPS
#obs.lon
#obs.lat
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

if moon_quarter < 2:
    moon_data['moon_phase'] = 'Waxing'
else:
    moon_data['moon_phase'] = 'Waning'

if moon_data['moon_phase'] == "Waxing":
    # waxing
    if moon_data["moon_phase_percent"] >= 0 and moon_data["moon_phase_percent"] < 15:
        moon_data['moon_phase_sign'] = '🌕'
    elif moon_data["moon_phase_percent"] >= 15 and moon_data["moon_phase_percent"] < 35:
        moon_data['moon_phase_sign'] = '🌔'
    elif moon_data["moon_phase_percent"] >= 35 and moon_data["moon_phase_percent"] < 65:
        moon_data['moon_phase_sign'] = '🌓'
    elif moon_data["moon_phase_percent"] >= 65 and moon_data["moon_phase_percent"] < 85:
        moon_data['moon_phase_sign'] = '🌒'
    elif moon_data["moon_phase_percent"] >= 85 and moon_data["moon_phase_percent"] <= 100:
        moon_data['moon_phase_sign'] = '🌑'
else:
    # waning
    if moon_data["moon_phase_percent"] >= 85 and moon_data["moon_phase_percent"] <= 100:
        moon_data['moon_phase_sign'] = '🌑'
    elif moon_data["moon_phase_percent"] >= 65 and moon_data["moon_phase_percent"] < 85:
        moon_data['moon_phase_sign'] = '🌘'
    elif moon_data["moon_phase_percent"] >= 35 and moon_data["moon_phase_percent"] < 65:
        moon_data['moon_phase_sign'] = '🌗'
    elif moon_data["moon_phase_percent"] >= 15 and moon_data["moon_phase_percent"] < 35:
        moon_data['moon_phase_sign'] = '🌖'
    elif moon_data["moon_phase_percent"] >= 0 and moon_data["moon_phase_percent"] < 15:
        moon_data['moon_phase_sign'] = '🌕'


for key in moon_data:
    print(f"{key} = {moon_data[key]}")


#print(f"Percent Illuminated: {round(moon_data['moon_phase_percent'])}%")





