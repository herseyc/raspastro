#########################################################
# Plot a map of the Solar System                        #
#########################################################
import numpy
from datetime import datetime
from raspastroinfo import AstroData
import matplotlib as mpl
import matplotlib.pyplot as plt
from rasp_calc_func import *


planets = AstroData()

planets.sun_info()

planets.planet_info()

planet_dict = {
    "Mercury": {
        "distance": planets.mercury['sun_distance'],
        "hlon": convert_dms_to_dd(planets.mercury['hlon']),
        "hlat": convert_dms_to_dd(planets.mercury['hlat']),
        "size": 1,
        "color": "brown",
    },
    "Venus": {
        "distance": planets.venus['sun_distance'],
        "hlon": convert_dms_to_dd(planets.venus['hlon']),
        "hlat": convert_dms_to_dd(planets.venus['hlat']),
        "size": 3,
        "color": "orange",
    },
    "Earth": {
        "distance": 1,
        "hlon": convert_dms_to_dd(planets.sun_data['earth_hlon']),
        "hlat": convert_dms_to_dd(planets.sun_data['earth_hlat']),
        "size": 3,
        "color": "green",
    },
    "Mars": {
        "distance": planets.mars['sun_distance'],
        "hlon": convert_dms_to_dd(planets.mars['hlon']),
        "hlat": convert_dms_to_dd(planets.mars['hlat']),
        "size": 3,
        "color": "red",
    },
    "Jupiter": {
        "distance": planets.jupiter['sun_distance'],
        "hlon": convert_dms_to_dd(planets.jupiter['hlon']),
        "hlat": convert_dms_to_dd(planets.jupiter['hlat']),
        "size": 10,
        "color": "purple",
    },
    "Saturn": {
        "distance": planets.saturn['sun_distance'],
        "hlon": convert_dms_to_dd(planets.saturn['hlon']),
        "hlat": convert_dms_to_dd(planets.saturn['hlat']),
        "size": 8,
        "color": "olive",
    },
    "Uranus": {
        "distance": planets.uranus['sun_distance'],
        "hlon": convert_dms_to_dd(planets.uranus['hlon']),
        "hlat": convert_dms_to_dd(planets.uranus['hlat']),
        "size": 7,
        "color": "cyan",
    },
    "Neptune": {
        "distance": planets.neptune['sun_distance'],
        "hlon": convert_dms_to_dd(planets.neptune['hlon']),
        "hlat": convert_dms_to_dd(planets.neptune['hlat']),
        "size": 7,
        "color": "blue",
    },
}

#print(planet_dict)

mpl.rcParams['xtick.color'] = 'white'
fig = plt.figure(figsize=(15,15), facecolor='black')
#ax = fig.add_subplot(projection='hammer', fc='black')
ax = fig.add_subplot(projection='polar', fc='black')
ax.set_theta_zero_location("SE")
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.grid(False)
ax.plot(0, 0, marker='o', markersize=20, color="yellow", label="Sun")
for key in planet_dict:
    ax.plot(numpy.deg2rad(planet_dict[key]['hlon']), planet_dict[key]['distance']+1, marker='o', markersize=planet_dict[key]['size'], color=planet_dict[key]['color'], label=key)
    #ax.plot(planet_dict[key]['hlon'], planet_dict[key]['hlat'], marker='o', markersize=planet_dict[key]['size'], color=planet_dict[key]['color'], label=key)

ax.legend()
plt.savefig('static/planets.png', bbox_inches='tight')

