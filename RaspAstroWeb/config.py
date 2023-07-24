# Store RaspAstro Configuration Variables

# Web Server Port
# Use this to change the port RaspAstroWeb listens on
WEBPORT = 5000

# Number of days to calculate ISS Passes
PASSDAYS = 5

#If USE_INDI is False then INDI Server info will not be queried
USE_INDI = False
 
# INDI Web Manager API Endpoint
INDIWEBMANAGER_API_ENDPOINT = "http://localhost:8624"

# Define Observer Horizon in DMS
MY_HORIZON = "0:0:0"

# Set to True to use GPS, False to use user configured lat/lon/elev
USE_GPS = False

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
        "M51|NGC 5194|UGC 8493|MCG 8-25-12|Whirlpool galaxy|PGC47404 N,f|G|S2,13:29:52.6,47:11:44,8.1,2000,672|414|7",
        "M81|NGC 3031|UGC 5318|MCG 12-10-10|Bode's nebulae|PGC28630 N,f|G|Sb,9:55:33.5,69:4:2,7,2000,1494|690|157",
        "M82|NGC 3034|UGC 5322|MCG 12-10-11|ARP 337|Ursa Major A|PGC28655 N,f|G|Sd,9:55:54,69:40:59,8.6,2000,672|258|65",
        "M104|NGC 4594|MCG -2-32-20|UGCA 293|Sombrero galaxy|PGC42407 N,f|G|Sa,12:39:59.3,-11:37:21,8.3,2000,516|252|89",
        "NGC 2403|UGC 3918|MCG 11-10-7|ZWG 309.40|ZWG 310.3|PGC21396 N,f|G|S6,7:36:50.6,65:36:6,8.2,2000,1404|708|127",
        "NGC 457|OCL 321,f|O|T1,1:19:35,58:17:12,6.4,2000,1200",
        "NGC 7635|LBN 549,f|N|EN,23:20:45,61:12:42,11,2000,900",
        "NGC 869|OCL 350|h Per|Double cluster,f|O|T1,2:19:0,57:7:42,5.3,2000,1080",
        "NGC 891|UGC 1831|MCG 7-5-46|ZWG 538.52|IRAS02195+4209|PGC9031 N,f|G|Sb,2:22:33,42:20:50,10.1,2000,702|96|22",
        "IC 434|LBN 953|CED 55N|Horsehead nebula,f|N|EN,5:41:0,-2:27:12,11,2000,3600",
        ]
