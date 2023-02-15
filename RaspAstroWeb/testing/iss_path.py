from datetime import datetime, timedelta

# Testing generating point to plot ISS path
# 9 path points with 10 minute between points will show 90 minutes
path_points = 9
minutes_between_points = 10


current_time = datetime.utcnow()

delta = current_time - timedelta(minutes=minutes_between_points)
while path_points > 0:
    # Call ISSData with delta time
    print(delta) 
    delta = delta - timedelta(minutes=minutes_between_points)
    # create path_coordinates list of tuples [(lat, lon)]
    # use folium.PolyLine(path_coordinates).add_to(m) to add path)
    path_points -= 1
