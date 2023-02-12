from flask import Flask, render_template
from raspissinfo import ISSData
from raspastroinfo import AstroData
from gps3 import agps3
import time
import math
from datetime import datetime
import folium
from rasp_calc_func import *
import time
import requests

app = Flask(__name__)

PASSDAYS = 5
INDIWEBMANAGER_API_ENDPOINT = "http://localhost:8624"

gps_data = []

def get_gps():
    # GPS Data
    the_connection = agps3.GPSDSocket()
    the_fix = agps3.DataStream()
    the_connection.connect()
    the_connection.watch()
    global gpslatitude
    global gpslongitude
    for new_data in the_connection:
       if new_data:
          the_fix.unpack(new_data)
          gpsfixtype = the_fix.mode
          gpslatitude = the_fix.lat
          gpslongitude = the_fix.lon
          gpsaltitude = the_fix.alt
          if the_fix.mode != "n/a" and the_fix.lat != "n/a" and the_fix.lon != "n/a":
             gpslatdms = convert_dd_to_dms(gpslatitude)
             gpslondms = convert_dd_to_dms(gpslongitude)
             # Make global so it can be used by other routes 
             global gps_data
             gps_data = [gpsfixtype, gpslatdms, gpslondms, gpsaltitude]
             break
          else:
             time.sleep(.5)
    the_connection.close()


@app.route('/')
def index():
    # Observer informaiton
    current_datetime = time_to_human(to_local(datetime.utcnow()))

    get_gps()

    obsm = folium.Map(location=[gpslatitude, gpslongitude], zoom_start=5)
    obsm.get_root().width = "450"
    obsm.get_root().height = "250px"
    obsm.get_root().render()
    folium.Marker(location=[gpslatitude, gpslongitude] , popup=f"Observer Location", icon=folium.Icon(color='blue', icon='user')).add_to(obsm)
    obsiframe = obsm.get_root()._repr_html_()


    # Sun/Moon/Planet/Information
    # AstroData from GPS
    astro = AstroData(obslat=gps_data[1], obslon=gps_data[2], obslev=gps_data[3])
    gps_data.append(astro.obs.horizon)

    astro.moon_info()
    astro.moon_data['next_full_moon'] = time_to_human(to_local(astro.moon_data['next_full_moon'].datetime()))
    astro.moon_data['next_new_moon'] = time_to_human(to_local(astro.moon_data['next_new_moon'].datetime()))

    astro.sun_info()
    astro.sun_data['next_sunset'] = time_to_human(to_local(astro.sun_data['next_sunset'].datetime()))
    astro.sun_data['next_sunrise'] = time_to_human(to_local(astro.sun_data['next_sunrise'].datetime()))
    astro.sun_data['next_solstice'] = time_to_human(to_local(astro.sun_data['next_solstice'].datetime()))
    astro.sun_data['next_equinox'] = time_to_human(to_local(astro.sun_data['next_equinox'].datetime()))

    astro.planet_info()

    return render_template('raspastrostatus.html', datetime=current_datetime,  gpsdata=gps_data, obsiframe=obsiframe, moon=astro.moon_data, sun=astro.sun_data, mercury=astro.mercury, venus=astro.venus, mars=astro.mars, jupiter=astro.jupiter, saturn=astro.saturn, uranus=astro.uranus, neptune=astro.neptune)

# INDI Info from INDI Web Manager API
@app.route('/indi')
def indi():
    indi_current = {}
    indi_status = requests.get(f"{INDIWEBMANAGER_API_ENDPOINT}/api/server/status")
    indi_status_data = indi_status.json()
    indi_current['status'] = indi_status_data[0]['status']
    indi_current['active_profile'] = indi_status_data[0]['active_profile']
    if indi_current['status']:
       driver_status = requests.get(f"{INDIWEBMANAGER_API_ENDPOINT}/api/server/drivers")
       driver_status_data = driver_status.json()
       driver_list = []

       for driver in driver_status_data:
           driver_list.append(driver['name'])
    else:
       driver_list = ["None"]


    return render_template('indi_iframe.html', indicurrent=indi_current, driverlist=driver_list)

@app.route('/iss')
def iss():
    current_datetime = time_to_human(to_local(datetime.utcnow()))

    # Get GPS data if we need to
    if len(gps_data) == 0:
       get_gps()

    # ISS Information
    iss = ISSData(obslat=gps_data[1], obslon=gps_data[2], obslev=gps_data[3])
    days = PASSDAYS
    iss.iss_passes(duration=days)
    iss_local = []
    iss_current = {}
    for i in iss.iss_next_passes:
        if not i['eclipsed'] and i['sun_alt'] < 0:
            iss_local.append({
                         "aos": time_to_human(to_local(i['aos'].datetime())), 
                         "los": time_to_human(to_local(i['los'].datetime())), 
                         "alt_max": round(math.degrees(i['alt_max']))})

    iss_current['geolat'] = iss.iss_telemetry.sublat
    iss_current['geolong'] = iss.iss_telemetry.sublong
    iss_current['elevation_miles'] = meters_to_miles(iss.iss_telemetry.elevation)

    lat_list = str(iss_current['geolat']).split(":")
    if lat_list[0] == '-':
      lat_dd = float(lat_list[0]) - float(lat_list[1])/60 - float(lat_list[2])/3600 
    else:
      lat_dd = float(lat_list[0]) + float(lat_list[1])/60 + float(lat_list[2])/3600 

    lon_list = str(iss_current['geolong']).split(":")
    if lon_list[0] == '-':
      lon_dd = float(lon_list[0]) - float(lon_list[1])/60 - float(lon_list[2])/3600 
    else:
      lon_dd = float(lon_list[0]) + float(lon_list[1])/60 + float(lon_list[2])/3600 

    m = folium.Map()
    m.get_root().width = "500"
    m.get_root().height = "300px"
    m.get_root().render()
    folium.Marker(location=[gpslatitude, gpslongitude] , popup=f"Observer Location", icon=folium.Icon(color='blue', icon='user')).add_to(m)
    folium.Marker(location=[lat_dd, lon_dd], popup=f"ISS Current Location at {current_datetime}", icon=folium.Icon(color='green', prefix='fa', icon='rocket')).add_to(m)
    #m.add_child(folium.Marker(location=[gpslatitude, gpslongitude] , popup=f"Observer Location", icon=folium.Icon(color='blue', icon='user')))
    #m.add_child(folium.Marker(location=[lat_dd, lon_dd], popup=f"ISS Current Location at {current_datetime}", icon=folium.Icon(color='green', prefix='fa', icon='rocket')))
    iframe = m.get_root()._repr_html_()

    return render_template('iss_iframe.html', datetime=current_datetime, iframe=iframe, isscurrent = iss_current, iss_pass_list=iss_local, duration=days)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
