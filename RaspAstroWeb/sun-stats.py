#########################################################
# Get informaiton about the Sun                         #
#########################################################
import numpy
from datetime import datetime
from raspastroinfo import AstroData
import matplotlib as mpl
import matplotlib.pyplot as plt
from gps3 import agps3
from rasp_calc_func import *
from config import *
from get_gps import *
import time


gps_data_tuple = get_gps_data()

gpsfixtype = gps_data_tuple[0]
gpslatdms = gps_data_tuple[1]
gpslondms = gps_data_tuple[2]
gpsaltitude = gps_data_tuple[3]
gpslatitude = gps_data_tuple[4]
gpslongitude = gps_data_tuple[5]
gps_data = gps_data_tuple[6]

sol = AstroData(obslat=gps_data[1], obslon=gps_data[2], obslev=gps_data[3], obshorizon=MY_HORIZON)

sol.sun_data = {}
sol.sun_info()

print(sol.sun_data)

