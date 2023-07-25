#!/usr/bin/env python3
from flask import Flask, render_template
from raspissinfo import ISSData
from raspastroinfo import AstroData
from gps3 import agps3
import time
import math
from datetime import datetime, timedelta
import folium
from rasp_calc_func import *
import time
import requests
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
from config import *
from get_gps import *


app = Flask(__name__)



# Moved to Function in get_gps.py
#gps_data = []
#
#def get_gps():
#    global gpslatitude
#    global gpslongitude
#    global gps_data
#    if USE_GPS:   
#        # GPS Data
#        the_connection = agps3.GPSDSocket()
#        the_fix = agps3.DataStream()
#        the_connection.connect()
#        the_connection.watch()
#        for new_data in the_connection:
#           if new_data:
#              the_fix.unpack(new_data)
#              if the_fix.mode != "n/a" and the_fix.lat != "n/a" and the_fix.lon != "n/a":
#                  gpsfixtype = the_fix.mode
#                  gpslatitude = the_fix.lat
#                  gpslongitude = the_fix.lon
#                  if gpsfixtype != 3:
#                      gpsaltitude = MY_ELEVATION
#                  else:
#                     gpsaltitude = the_fix.alt
#
#                  gpslatdms = convert_dd_to_dms(gpslatitude)
#                  gpslondms = convert_dd_to_dms(gpslongitude)
#                  gps_data = [gpsfixtype, gpslatdms, gpslondms, gpsaltitude]
#                  break
#              else:
#                 time.sleep(.5)
#
#        the_connection.close()
#    else:
#        gpsfixtype = "MANUAL"
#        gpslatdms = MY_LAT
#        gpslondms = MY_LON
#        gpsaltitude = MY_ELEVATION
#        gps_data = [gpsfixtype, gpslatdms, gpslondms, gpsaltitude]
#        gpslatitude = convert_dms_to_dd(MY_LAT)
#        gpslongitude = convert_dms_to_dd(MY_LON)
        
#Moon Images
moon_image = {
    "Waxing": {
        "New Moon": "NewMoon",
        "Crescent": "WaxingCrescent",
        "Gibbous": "WaxingGibbous",
        "First Quarter": "FirstQuarter",
        "Full Moon": "FullMoon",
    },
    "Waning": {
        "Full Moon": "FullMoon",
        "Crescent": "WaningCrescent",
        "Gibbous": "WaningGibbous",
        "Last Quarter": "LastQuarter",
        "New Moon": "NewMoon",
    },
}
        


@app.route('/')
def index():
    # Observer informaiton
    current_utctime = datetime.utcnow()
    current_datetime = time_to_human(to_local(current_utctime))

    gps_data_tuple = get_gps_data()

    gpsfixtype = gps_data_tuple[0]
    gpslatdms = gps_data_tuple[1]
    gpslondms = gps_data_tuple[2]
    gpsaltitude = gps_data_tuple[3]
    gpslatitude = gps_data_tuple[4]
    gpslongitude = gps_data_tuple[5]
    gps_data = gps_data_tuple[6]

    obsm = folium.Map(location=[gpslatitude, gpslongitude], zoom_start=5)
    obsm.get_root().width = "450"
    obsm.get_root().height = "250px"
    obsm.get_root().render()
    folium.Marker(location=[gpslatitude, gpslongitude] , popup=f"Observer Location", icon=folium.Icon(color='blue', icon='user')).add_to(obsm)
    obsiframe = obsm.get_root()._repr_html_()


    # Sun/Moon/Planet/Information
    # AstroData from GPS
    astro = AstroData(obslat=gps_data[1], obslon=gps_data[2], obslev=gps_data[3], obshorizon=MY_HORIZON)
    gps_data.append(astro.obs.horizon)

    # Moon Information
    astro.moon_info()
    astro.moon_data['next_full_moon'] = time_to_human(to_local(astro.moon_data['next_full_moon'].datetime()))
    astro.moon_data['next_new_moon'] = time_to_human(to_local(astro.moon_data['next_new_moon'].datetime()))

    # Is Moon Rising or Setting
    astro.moon_data['rising_sign'] = rising_or_setting(astro.moon_data['next_moon_transit'])
    astro.moon_data['next_moon_transit'] = time_to_human(to_local(astro.moon_data['next_moon_transit'].datetime()))

    # Sun Information
    astro.sun_info()
    astro.sun_data['next_sunset'] = time_to_human(to_local(astro.sun_data['next_sunset'].datetime()))
    astro.sun_data['next_sunrise'] = time_to_human(to_local(astro.sun_data['next_sunrise'].datetime()))
    astro.sun_data['next_solstice'] = time_to_human(to_local(astro.sun_data['next_solstice'].datetime()))
    astro.sun_data['next_equinox'] = time_to_human(to_local(astro.sun_data['next_equinox'].datetime()))

    # Is Sun Rising or Setting
    astro.sun_data['rising_sign'] = rising_or_setting(astro.sun_data['next_sun_transit'])

    astro.sun_data['next_sun_transit'] = time_to_human(to_local(astro.sun_data['next_sun_transit'].datetime()))

    # Get Deep Sky Custom Object Info
    # A list of XEphem formated data in config.py
    #set dict for results
    custom_deepsky = {}
    for edbobject in CUSTOM_OBJECTS:
        astro.object_info(catalog=edbobject)
        object_name = astro.object_data['name'].split("|")
        astro.object_data['alt'] = round(math.degrees(astro.object_data['alt']), 1)
        astro.object_data['az'] = round(math.degrees(astro.object_data['az']), 1)
        astro.object_data['rising_sign'] = rising_or_setting(astro.object_data['next_transit'])

        astro.object_data['next_transit'] = time_to_human(to_local(astro.object_data['next_transit'].datetime()))
        custom_deepsky[object_name[0]] = astro.object_data 

    # Get Planet Info
    astro.planet_info()

    #Figure out if planet is rizing or setting

    # Messier Objects
    messier_objs = {}
    messier_list = []
    messier_file = "./xephemcat/Messier.edb"
    with open(messier_file) as lines:
        for obj in lines:
            if not obj.strip().startswith("#"):
                messier_list.append(obj)

    for messier_obj in messier_list:
        astro.object_info(catalog=messier_obj)
        messier_object_name = astro.object_data['name'].split("|")
        astro.object_data['alt'] = round(math.degrees(astro.object_data['alt']), 1)
        astro.object_data['az'] = round(math.degrees(astro.object_data['az']), 1)
        # Is the object rising or setting
        astro.object_data['rising_sign'] = rising_or_setting(astro.object_data['next_transit'])

        astro.object_data['next_transit'] = time_to_human(to_local(astro.object_data['next_transit'].datetime()))
        messier_objs[messier_object_name[0]] = astro.object_data 

    # Get Polaris Info
    astro.polaris_info()

    # Generate Polar Align Image
    phourangle = numpy.deg2rad(astro.polaris_data['phourangle'])
    mpl.rcParams['xtick.color'] = 'white'
    fig = plt.figure(facecolor='black')
    ax = fig.add_subplot(projection='polar', fc='black')
    # Flip it around since polar scope image is inverted
    ax.set_theta_zero_location("S")
    ax.set_yticklabels([])
    ax.text(0,0, "NCP", fontdict={"fontsize": "medium", "color": "white", "family": "monospace", "fontweight": "bold"})
    ax.plot(phourangle, 1, marker='o', markersize=10.2, color='red', label='Polaris')
    plt.savefig('./static/polarisalign.png', bbox_inches='tight')
    astro.polaris_data['phourangle'] = int(astro.polaris_data['phourangle'])
    astro.polaris_data['next_transit'] = time_to_human(to_local(astro.polaris_data['next_transit'].datetime()))
    astro.polaris_data['hourangle'] = round(astro.polaris_data['phourangle'] * 0.0667, 1)

    return render_template('raspastrostatus.html', datetime=current_datetime,  gpsdata=gps_data, gpslatdec=f"{gpslatitude:.2f}", gpslondec=f"{gpslongitude:.2f}", obsiframe=obsiframe, moon=astro.moon_data, moonimage=moon_image, sun=astro.sun_data, mercury=astro.mercury, venus=astro.venus, mars=astro.mars, jupiter=astro.jupiter, saturn=astro.saturn, uranus=astro.uranus, neptune=astro.neptune, polaris=astro.polaris_data, deepsky=custom_deepsky, messier=messier_objs)

# INDI Info from INDI Web Manager API
@app.route('/indi')
def indi():
    indi_current = {}
    driver_list = []
    # Pull AstroData for local host name
    astrohost = get_hostname()
    if USE_INDI:
        indi_status = requests.get(f"{INDIWEBMANAGER_API_ENDPOINT}/api/server/status")
        indi_status_data = indi_status.json()
        indi_current['status'] = indi_status_data[0]['status']
        indi_current['active_profile'] = indi_status_data[0]['active_profile']
        if indi_current['status']:
           driver_status = requests.get(f"{INDIWEBMANAGER_API_ENDPOINT}/api/server/drivers")
           driver_status_data = driver_status.json()

           for driver in driver_status_data:
               driver_list.append(driver['name'])
        else:
           driver_list = ["None"]
    else:
        indi_current['status'] = "Not Used"
        driver_list = ["None"]

    return render_template('indi_iframe.html', indicurrent=indi_current, driverlist=driver_list, astrohost=astrohost)

@app.route('/iss')
def iss():
    current_datetime = time_to_human(to_local(datetime.utcnow()))
    current_utctime = datetime.utcnow()

    # Get observer GPS data
    gps_data_tuple = get_gps_data()

    gpsfixtype = gps_data_tuple[0]
    gpslatdms = gps_data_tuple[1]
    gpslondms = gps_data_tuple[2]
    gpsaltitude = gps_data_tuple[3]
    gpslatitude = gps_data_tuple[4]
    gpslongitude = gps_data_tuple[5]
    gps_data = gps_data_tuple[6]

    # ISS Information
    iss = ISSData(obslat=gps_data[1], obslon=gps_data[2], obslev=gps_data[3], obshorizon=MY_HORIZON)
    days = PASSDAYS
    iss.iss_passes(duration=days)
    iss_local = []
    iss_current = {}
    for i in iss.iss_next_passes:
        if not i['eclipsed'] and i['sun_alt'] < 0:
            iss_local.append({
                         "aos": time_to_human(to_local(i['aos'].datetime())), 
                         "los": time_to_human(to_local(i['los'].datetime())), 
                         "alt_max": round(math.degrees(i['alt_max'])),
                         "constellation": i['constellation'][1],
                         })

    iss_current['geolat'] = iss.iss_telemetry.sublat
    iss_current['geolong'] = iss.iss_telemetry.sublong
    iss_current['range'] = meters_to_miles(iss.iss_telemetry.range)
    iss_current['range_velocity'] = round(meters_to_miles(iss.iss_telemetry.range_velocity * 3600), 2) 
    iss_current['elevation_miles'] = meters_to_miles(iss.iss_telemetry.elevation)

    lat_dd = convert_dms_to_dd(iss_current['geolat'])
    lon_dd = convert_dms_to_dd(iss_current['geolong'])

    #lat_list = str(iss_current['geolat']).split(":")
    #if lat_list[0] == '-':
    #  lat_dd = float(lat_list[0]) - float(lat_list[1])/60 - float(lat_list[2])/3600 
    #else:
    #  lat_dd = float(lat_list[0]) + float(lat_list[1])/60 + float(lat_list[2])/3600 

    #lon_list = str(iss_current['geolong']).split(":")
    #if lon_list[0] == '-':
    #   lon_dd = float(lon_list[0]) - float(lon_list[1])/60 - float(lon_list[2])/3600 
    #else:
    #  lon_dd = float(lon_list[0]) + float(lon_list[1])/60 + float(lon_list[2])/3600 

    m = folium.Map()
    m.get_root().width = "500"
    m.get_root().height = "300px"
    folium.Marker(location=[gpslatitude, gpslongitude] , popup=f"Observer Location", icon=folium.Icon(color='blue', icon='user')).add_to(m)
    folium.Marker(location=[lat_dd, lon_dd], popup=f"ISS Current Location at {current_datetime}", icon=folium.Icon(color='green', prefix='fa', icon='rocket')).add_to(m)

    # Display ISS previous path
    path_points = 120
    seconds_between_points = 30
    delta = current_utctime - timedelta(seconds=seconds_between_points)
    while path_points > 0:
        isspath = ISSData(obslat=gps_data[1], obslon=gps_data[2], obslev=gps_data[3], obsepoch=delta)
        delta = delta - timedelta(seconds=seconds_between_points)
        folium.CircleMarker(location=[convert_dms_to_dd(isspath.iss_telemetry.sublat), convert_dms_to_dd(isspath.iss_telemetry.sublong)], radius=1, fill_color="#ECFFDC", fill=True, color="#ECFFDC").add_to(m)
        path_points -= 1

    # Display ISS future path
    # TODO: Need to figure out how to keep path from wrapping back on
    # itself when it crosses edge of map.
    path_points = 90
    delta = current_utctime + timedelta(seconds=seconds_between_points)
    while path_points > 0:
        isspath = ISSData(obslat=gps_data[1], obslon=gps_data[2], obslev=gps_data[3], obsepoch=delta)
        delta = delta + timedelta(seconds=seconds_between_points)
        folium.CircleMarker(location=[convert_dms_to_dd(isspath.iss_telemetry.sublat), convert_dms_to_dd(isspath.iss_telemetry.sublong)], radius=1, fill_color="#BEBEBE", fill=True, color="#BEBEBE").add_to(m)
        path_points -= 1

    m.get_root().render()
    iframe = m.get_root()._repr_html_()

    return render_template('iss_iframe.html', datetime=current_datetime, iframe=iframe, isscurrent = iss_current, iss_pass_list=iss_local, duration=days)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=WEBPORT)
