from raspastroinfo import AstroData
import math
from rasp_calc_func import *
import ephem
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt



polaris = AstroData()

print(time_to_human(to_local(polaris.obs.date.datetime())))

polaris.polaris_info()

phourangle = numpy.deg2rad(polaris.polaris_data['phourangle'])
print(f"phourangle = {polaris.polaris_data['phourangle']}")

mpl.rcParams['xtick.color'] = 'white' 
fig = plt.figure(facecolor='black')
ax = fig.add_subplot(projection='polar', fc='black')
ax.set_theta_zero_location("S")
ax.set_yticklabels([])
ax.plot(phourangle, 1, marker='o', markersize=10.2, color='red', label='Polaris')

plt.savefig('static/polarisalign.png', bbox_inches='tight')


print("Distance from Celestial Pole")
print(polaris.polaris_data['from_pole'])
print("Next Polaris Transit")
print(time_to_human(to_local(polaris.polaris_data['next_transit'].datetime())))
