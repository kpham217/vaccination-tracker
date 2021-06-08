import requests
import csv

import json
from datetime import datetime,date
import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler("PyH1EDxN8aRvU7nZ2gGBfqkDG",
    "WEZueY7AR585u1PaH2pgeBDoXBqUYSIevrVm5QxxdLVaU3YdB3")
auth.set_access_token("1401205897699938308-NrjWBTHUWk5puJOcZJqjpr8g8M13NF",
    "ORT2D6vLsURaW7fdAvI11whd3U69v2aVr0hAZMlBwSo9b")

api = tweepy.API(auth)



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
with open ('F:/PycharmProjects/vaccination-tracker/scraping-script/population density data/Halifax.csv','r') as csv_file:
    reader =csv.reader(csv_file)
    next(reader) # skip first row
    for row in reader:
        halifax_id.append(row[0])
print(halifax_id)


def tweet(site):
    try:
        api.verify_credentials()
        api.update_status(site)
        print("Authentication OK")
    except:
        print("Error during authentication")


def requestBookingTime(id_list):
    try:
        for item in id_list:
            request = "https://sync-cf2-1.canimmunize.ca/fhir/v1/public/availability/17430812-2095-4a35-a523-bb5ce45d60f1?appointmentTypeId=" + item['id'] +"&timezone=America%2FHalifax&preview=false"

            result = requests.get(
            request)
            bookingdata = result.text
            # print(bookingdata)
            json_bookingData = json.loads(bookingdata)[0]["availabilities"]
            closest = json_bookingData[0]['time'] [:len(json_bookingData[0]['time'])-5] +'Z'
            item['bookingTime'] = closest
            # print(json_bookingData['time'][0])
    except:
        print("An exception occurred")
    return id_list
# 2018-09-05T14:09:03Z
# 2021-06-17T12:00:00Z
def cross_check(id):
    for item in json_data:
        if item['fullyBooked'] == False and item['id'] == id:
            return True
    return False

def name_search(id):
    for item in json_data:
        if item['id'] == id:
            return item['durationDisplayEn']


def calculate_time_score(list):
    list.sort(key = lambda item: datetime.strptime(item['bookingTime'],"%Y-%m-%dT%H:%M:%SZ"))
    earlies = datetime.strptime(list[0]['bookingTime'],"%Y-%m-%dT%H:%M:%SZ")
    furthest = datetime.strptime(list[len(list)-1]['bookingTime'],"%Y-%m-%dT%H:%M:%SZ")
    delta = earlies - furthest

    for item in list:
        bPoint = datetime.strptime(item['bookingTime'],"%Y-%m-%dT%H:%M:%SZ")
        item['bookingTimeScore'] = (bPoint - furthest) / delta * 100
    return list
# halifax_objects.append({'id': halifax_id[0], 'bookingTime': 'ASD 1500', 'bookingTimeScore' : 'asdasd'})
for index in range(len(halifax_id)):
    if cross_check(halifax_id[index]):
        halifax_objects.append({'id' : halifax_id[index], 'bookingTime': '', 'bookingTimeScore': '', 'siteName': ''})

# print(halifax_objects[0])
updated_halifax_object = requestBookingTime(halifax_objects)
# print(updated_halifax_object)
updated_halifax_object_2=calculate_time_score(updated_halifax_object)
# print(updated_halifax_object_2)
updated_halifax_object_2 = updated_halifax_object_2[0:5]
# print(updated_halifax_object_2)

for i in updated_halifax_object_2:
    print(i['id'])
    i['siteName'] = name_search(i['id'])
    tweet(i['siteName'])

print(updated_halifax_object_2)

# print(halifax_objects[3]['id'])
# print(len(halifax_objects))
# for item in json_data:
#     if item["fullyBooked"] == False and "Halifax" in item["durationDisplayEn"].split(",")[1]:
#         print(item["durationDisplayEn"])