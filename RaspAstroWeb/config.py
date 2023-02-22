# Store RaspAstro Configuration Variables

# Number of days to calculate ISS Passes
PASSDAYS = 5

#If USE_INDI is False then INDI Server info will not be queried
USE_INDI = True
 
# INDI Web Manager API Endpoint
INDIWEBMANAGER_API_ENDPOINT = "http://localhost:8624"

# Define Observer Horizon in DMS
MY_HORIZON = "0:0:0"

# Set to True to use GPS, False to use user configured lat/lon/elev
USE_GPS = True

# If USE_GPS is False use the following for observer location
# Latitude and Longitude DMS string
MY_LAT = "36:46:46.0"
MY_LON = "-76:32:8.1"

# Observer Elevation (float in meters)
MY_ELEVATION = 7.7

# Define custom objests for Deep Sky Tab
# Use XEphem formated data
# https://github.com/XEphem/Catalogs 
CUSTOM_OBJECTS = [
        "M1|NGC 1952|LBN 833|Sh2-244|CED 53|Taurus A,f|R|SN,5:34:31.9,22:0:52,8.4,2000,360",
        "M33|NGC 598|UGC 1117|MCG 5-4-69|ZWG 502.110|PGC5818 N,f|G|Sc,1:33:51.9,30:39:29,5.5,2000,4122|2496|23",
        "M42|NGC 1976|LBN 974|Orion nebula,f|N|EN,5:35:17.1,-5:23:25,4,2000,3900",
        "IC 434|LBN 953|CED 55N|Horsehead nebula,f|N|EN,5:41:0,-2:27:12,11,2000,3600",
        "M81|NGC 3031|UGC 5318|MCG 12-10-10|Bode's nebulae|PGC28630 N,f|G|Sb,9:55:33.5,69:4:2,7,2000,1494|690|157",
        "NGC 2403|UGC 3918|MCG 11-10-7|ZWG 309.40|ZWG 310.3|PGC21396 N,f|G|S6,7:36:50.6,65:36:6,8.2,2000,1404|708|127",
        "NGC 457|OCL 321,f|O|T1,1:19:35,58:17:12,6.4,2000,1200",
        ]
