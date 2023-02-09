from flask import Flask, render_template
from raspissinfo import ISSData
from raspastroinfo import AstroData
import time
from datetime import datetime
import folium
from rasp_calc_func import *

app = Flask(__name__)

@app.route('/')
def index():
    current_datetime = time_to_human(to_local(datetime.utcnow()))
    # ISS Information
    iss = ISSData()
    iss_next_passes = iss.iss_passes(duration=3)
    iss_local = []
    iss_current = {}
    for i in iss_next_passes:
        if not i['eclipsed']:
            iss_local.append({"aos": time_to_human(to_local(i['aos'].datetime())), "los": time_to_human(to_local(i['los'].datetime()))})

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

    m = folium.Map()
    m.get_root().width = "500"
    m.get_root().height = "300px"
    m.get_root().render()
    m.add_child(folium.Marker(location=[lat_dd, lon_dd], popup=f"ISS Current Location at {current_datetime}", icon=folium.Icon(color='green')))
    iframe = m.get_root()._repr_html_()
    
    # Sun/Moon/Information
    astro = AstroData()
    moon_data = astro.moon_info()
    moon_data['next_full_moon'] = time_to_human(to_local(moon_data['next_full_moon'].datetime()))
    moon_data['next_new_moon'] = time_to_human(to_local(moon_data['next_new_moon'].datetime()))
    sun_data = astro.sun_info()
    sun_data['next_sunset'] = time_to_human(to_local(sun_data['next_sunset'].datetime()))
    sun_data['next_sunrise'] = time_to_human(to_local(sun_data['next_sunrise'].datetime()))
    sun_data['next_solstice'] = time_to_human(to_local(sun_data['next_solstice'].datetime()))
    sun_data['next_equinox'] = time_to_human(to_local(sun_data['next_equinox'].datetime()))
    return render_template('raspastrostatus.html', iframe=iframe, datetime=current_datetime, isscurrent = iss_current, iss_pass_list=iss_local, moon=moon_data, sun=sun_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
