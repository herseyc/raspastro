from raspastroinfo import AstroData
from datetime import datetime
import math
from rasp_calc_func import *


astro = AstroData()

astro.planet_info()

print("Mercury")
for key in astro.mercury:
    print(f"{key}: {astro.mercury[key]}")

print("Venus")
for key in astro.venus:
    print(f"{key}: {astro.venus[key]}")

print("Mars")
for key in astro.mars:
    print(f"{key}: {astro.mars[key]}")

print("Jupiter")
for key in astro.jupiter:
    print(f"{key}: {astro.jupiter[key]}")

print("Saturn")
for key in astro.saturn:
    print(f"{key}: {astro.saturn[key]}")

print("Uranus")
for key in astro.uranus:
    print(f"{key}: {astro.uranus[key]}")

print("Neptune")
for key in astro.neptune:
    print(f"{key}: {astro.neptune[key]}")
