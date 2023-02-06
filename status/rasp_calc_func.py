########################################################
# Just some different calculations for RaspAstro       #
########################################################

########################################
# function to convert UTC to localtime #
########################################
def to_local(time):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    time = time.replace(tzinfo=from_zone)
    local_time = time.astimezone(to_zone)
    return local_time

########################################
# function to convert Meters to Miles  #
########################################
def meters_to_miles(meters):
    miles = round(meters / 1609, 2)
    return miles

