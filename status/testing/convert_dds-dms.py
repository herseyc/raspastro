
MY_LAT = 36.7794571 # Your latitude
MY_LON = -76.5355366 # Your longitude

list = [MY_LAT, MY_LON]

for dd in list:
    print(dd)
    degrees = int(dd)
    temp = 60 * (dd - degrees)
    minutes = int(temp)
    seconds = round(60 * (temp - minutes), 4)
    dms = f"{degrees}:{abs(minutes)}:{abs(seconds)}"
    print(dms)


