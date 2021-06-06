import requests
import csv

import json
from datetime import datetime

class BookingInfo(object):
    def __init__(self, id,bookingTime,bookingTimeScore):
        self.id = id
        self.bookingTime = bookingTime
        self.bookingTimeScore= bookingTimeScore

data = {}
json_data = []
try:
    r = requests.get(
        'https://sync-cf2-1.canimmunize.ca/fhir/v1/public/booking-page/17430812-2095-4a35-a523-bb5ce45d60f1/appointment-types?forceUseCurrentAppointment=false&preview=false')
    # data = r.text.results
    data = r.text
    json_data = json.loads(data)["results"]
except:
  print("An exception occurred")

# print("Halifax" in json_data[1]["gisLocationString"])


halifax_id = []
halifax_objects =[]
with open ('./county-csv/Halifax_id.csv','r') as csv_file:
    reader =csv.reader(csv_file)
    next(reader) # skip first row
    for row in reader:
        halifax_id.append(row[0])
print(halifax_id)
def requestBookingTime(id_list):
    try:
        for item in id_list:
            request = "https://sync-cf2-1.canimmunize.ca/fhir/v1/public/availability/17430812-2095-4a35-a523-bb5ce45d60f1?appointmentTypeId=" + item['id'] +"&timezone=America%2FHalifax&preview=false"

            result = requests.get(
            request)
            bookingdata = result.text
            # print(bookingdata)
            json_bookingData = json.loads(bookingdata)[0]["availabilities"]
            closest = json_bookingData[0]['time']
            item['bookingTime'] = closest
            # print(json_bookingData['time'][0])
    except:
        print("An exception occurred")
    return id_list
def cross_check(id):
    for item in json_data:
        if item['fullyBooked'] == False and item['id'] == id:
            return True
    return False
# def calculate_time_score(list):
#     list.sort(key = lambda item: item['bookingTime'].strptime(i))
# halifax_objects.append({'id': halifax_id[0], 'bookingTime': 'ASD 1500', 'bookingTimeScore' : 'asdasd'})
for index in range(len(halifax_id)):
    if cross_check(halifax_id[index]):
        halifax_objects.append({'id' : halifax_id[index], 'bookingTime': '', 'bookingTimeScore': ''})

print(halifax_objects[0])
updated_halifax_object = requestBookingTime(halifax_objects)
print(updated_halifax_object)
# print(halifax_objects[3]['id'])
# print(len(halifax_objects))
# for item in json_data:
#     if item["fullyBooked"] == False and "Halifax" in item["durationDisplayEn"].split(",")[1]:
#         print(item["durationDisplayEn"])