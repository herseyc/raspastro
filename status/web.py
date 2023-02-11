from flask import Flask, render_template
from raspissinfo import ISSData
from raspastroinfo import AstroData
import time
import math
from datetime import datetime
import folium
from rasp_calc_func import *

app = Flask(__name__)


indi_running = ["MAYBE"]

@app.route('/')
def index():
    current_datetime = time_to_human(to_local(datetime.utcnow()))

    # Sun/Moon/Information
    astro = AstroData()
    astro.moon_info()
    astro.moon_data['next_full_moon'] = time_to_human(to_local(astro.moon_data['next_full_moon'].datetime()))
    astro.moon_data['next_new_moon'] = time_to_human(to_local(astro.moon_data['next_new_moon'].datetime()))
    astro.sun_info()
    astro.sun_data['next_sunset'] = time_to_human(to_local(astro.sun_data['next_sunset'].datetime()))
    astro.sun_data['next_sunrise'] = time_to_human(to_local(astro.sun_data['next_sunrise'].datetime()))
    astro.sun_data['next_solstice'] = time_to_human(to_local(astro.sun_data['next_solstice'].datetime()))
    astro.sun_data['next_equinox'] = time_to_human(to_local(astro.sun_data['next_equinox'].datetime()))

    return render_template('raspastrostatus.html', datetime=current_datetime, moon=astro.moon_data, sun=astro.sun_data, indi=indi_running)


@app.route('/iss')
def iss():
    current_datetime = time_to_human(to_local(datetime.utcnow()))
    # ISS Information
    iss = ISSData()
    iss.iss_passes(duration=3)
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
    if lat_list[0] == '-':
      lon_dd = float(lon_list[0]) - float(lon_list[1])/60 - float(lon_list[2])/3600 
    else:
      lon_dd = float(lon_list[0]) + float(lon_list[1])/60 + float(lon_list[2])/3600 

    obslat = str(iss.obs.lat).split(":")
    if obslat[0] == '-':
      obslat_dd = float(obslat[0]) - float(obslat[1])/60 - float(obslat[2])/3600 
    else:
      obslat_dd = float(obslat[0]) + float(obslat[1])/60 + float(obslat[2])/3600 
    obslon = str(iss.obs.lon).split(":")
    if obslon[0] == '-':
      obslon_dd = float(obslon[0]) - float(obslon[1])/60 - float(obslon[2])/3600 
    else:
      obslon_dd = float(obslon[0]) + float(obslon[1])/60 + float(obslon[2])/3600 

    m = folium.Map()
    m.get_root().width = "500"
    m.get_root().height = "300px"
    m.get_root().render()
    m.add_child(folium.Marker(location=[lat_dd, lon_dd], popup=f"ISS Current Location at {current_datetime}", icon=folium.Icon(color='green', prefix='fa', icon='rocket')))
    m.add_child(folium.Marker(location=[obslat_dd, obslon_dd] , popup=f"Observer Location", icon=folium.Icon(color='blue', icon='user')))
    iframe = m.get_root()._repr_html_()

    return render_template('iss_iframe.html', datetime=current_datetime, iframe=iframe, isscurrent = iss_current, iss_pass_list=iss_local)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
