
MY_LAT = 36.7794571 # Your latitude
MY_LON = -76.5355366 # Your longitude

def convert_ddstodms(dd):
    degrees = int(dd)
    temp = 60 * (dd - degrees)
    minutes = int(temp)
    seconds = round(60 * (temp - minutes), 1)
    dms = f"{degrees}:{abs(minutes)}:{abs(seconds)}"
    return dms

print(convert_ddstodms(MY_LAT))
print(convert_ddstodms(MY_LON))
