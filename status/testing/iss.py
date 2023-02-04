from urllib import request
from datetime import datetime
import ephem

iss_tledata = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
f = request.urlopen(iss_tledata)
iss = f.read()

print(iss)


#iss = ephem.readtle('ISS (ZARYA)', '1 25544U 98067A   23035.56371721  .00019294  00000+0  34975-3 0  9990', '2 25544  51.6423 265.4314 0008372 312.5319 130.6015 15.49599083381227')


