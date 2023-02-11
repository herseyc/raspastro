This is a work in progress

## raspastro-web.py
Flash app to display data on webpage. To run:

```
python3 raspastro-web.py
```

Will listen on port 5000, so just access at http://ipofdevice:5000 
Currently requires GPS data, but I will probably update to allow you to define.

## raspissinfo.py
ISSData Class to get ISS current information and determine next passes for observer location.

## raspastroinfo.py
AstroData Class to get information related to the Sun and Moon for an oberserver location

## rasp_calc_func.py
Functions to convert UTC to local time (to_local(time)), convert meters to miles (meters_to_miles(meters)), and determine is a UTC datetime is at night in local time (is_at_night(checkdate, lat, lon) for a specific location.

## examples.py
Examples for using the ISSData Class and AstroData Class as well as the rasp_calc_func.py
