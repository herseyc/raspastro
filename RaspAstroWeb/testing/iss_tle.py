from datetime import datetime

file_path = "isstle.data"

current_time = datetime.now()

weekday = current_time.weekday()

with open(file_path) as filetle:
    line = filetle.readline()

tle_data_list = line.split("|")

print(weekday)
print(tle_data_list[0])
print(tle_data_list[1])
print(tle_data_list[2])
print(tle_data_list[3])

if int(tle_data_list[0]) == weekday:
    print("Equal")
else:
    print("Not Equal")

c_time = datetime.now().weekday() + 1
print(c_time)
