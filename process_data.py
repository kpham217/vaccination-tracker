import requests
import json
from datetime import datetime


def create_eligible_list(ref_list, updated_list):
    print("> Create list of eligible sites based on Fully-Booked status")

    def cross_check(ref_id, list2compare):
        for i in list2compare:
            # NEW: only check fullyBooked once when ID is matched
            if i['id'] != ref_id:
                continue

            if not i['fullyBooked']:
                return True, i['durationDisplayEn']
            else:
                return False, None

        #      OLD: have to check twice if 'fullyBooked' == False (check fullyBooked then check ID)
        #     if not i['fullyBooked'] and i['id'] == item:
        #         return True
        # return False

    site_list = []
    for item in ref_list:
        stt, site_name = cross_check(item, updated_list)
        if stt:
            site_list.append({'id': item, 'bookingTime': '', 'bookingTimeScore': '', 'readableBookingTime': '', 'siteName': site_name})

    return site_list


def request_booking_time(site_list, booking_time_link):
    print("> Request booking time for each site")
    for item in site_list:
        request = booking_time_link[0] + item['id'] + booking_time_link[1]
        result = requests.get(request)
        bookingdata = result.text
        # print(bookingdata)
        json_booking_data = json.loads(bookingdata)[0]["availabilities"]
        closest = json_booking_data[0]['time'][:len(json_booking_data[0]['time'])-5] + 'Z'
        item['bookingTime'] = closest

    return site_list


def calculate_time_score(site_list):
    print("> Scoring each site based on its nearest available date")
    site_list.sort(key=lambda i: datetime.strptime(i['bookingTime'], "%Y-%m-%dT%H:%M:%SZ"))
    earliest = datetime.strptime(site_list[0]['bookingTime'], "%Y-%m-%dT%H:%M:%SZ")
    furthest = datetime.strptime(site_list[len(site_list)-1]['bookingTime'], "%Y-%m-%dT%H:%M:%SZ")
    delta = earliest - furthest

    for item in site_list:
        b_point = datetime.strptime(item['bookingTime'],"%Y-%m-%dT%H:%M:%SZ")
        item['bookingTimeScore'] = (b_point - furthest) / delta * 100
        item['readableBookingTime'] = b_point.strftime('%a, %d %b %Y %H:%M:%S')
    return site_list


def processing(ref_list, updated_list, booking_time_link):
    available_site_list = create_eligible_list(ref_list, updated_list)
    available_site_list = request_booking_time(available_site_list, booking_time_link)
    available_site_list = calculate_time_score(available_site_list)
    return available_site_list[0:5]
