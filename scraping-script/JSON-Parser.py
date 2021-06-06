import requests

import json

data = {}
try:
    r = requests.get(
        'https://sync-cf2-1.canimmunize.ca/fhir/v1/public/booking-page/17430812-2095-4a35-a523-bb5ce45d60f1/appointment-types?forceUseCurrentAppointment=false&preview=false')
    # data = r.text.results
    data = r.text
    json_data = json.loads(data)["results"]
except:
  print("An exception occurred")

# print("Halifax" in json_data[1]["gisLocationString"])
for item in json_data:
    if item["fullyBooked"] == False and "Halifax" in item["durationDisplayEn"].split(",")[1]:
        print(item["durationDisplayEn"])