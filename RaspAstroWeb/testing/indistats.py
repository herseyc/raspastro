import requests


# Access API of INDI Web Manager

indi_status = requests.get("http://localhost:8624/api/server/status")
indi_status_data = indi_status.json()
print(f"Status: {indi_status_data[0]['status']}")
print(f"Profile: {indi_status_data[0]['active_profile']}")


driver_status = requests.get("http://localhost:8624/api/server/drivers")
driver_status_data = driver_status.json()

for driver in driver_status_data:
    print("-------------------")
    for key in driver:
        print(f"{key} {driver[key]}")
