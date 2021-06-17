import requests
import json
from datetime import datetime
import pytz
# import datetime
local_tz = pytz.timezone('America/Halifax') # use your local timezone name here


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
    if not site_list:
        return site_list
    for index, item in enumerate(site_list):
        request = booking_time_link[0] + item['id'] + booking_time_link[1]
        # print(request)
        result = requests.get(request)
        bookingdata = result.text
        # print(bookingdata)
        try:
            json_booking_data = json.loads(bookingdata)[0]["availabilities"]
            closest = json_booking_data[0]['time'][:len(json_booking_data[0]['time'])-5] + 'Z'
            item['bookingTime'] = closest
        except IndexError:
            print('IndexError: no available data for this vax site')

    result = [i for i in site_list if i['bookingTime'] != '']
    return result


def calculate_time_score(site_list):
    print("> Scoring each site based on its nearest available date")
    if not site_list:
        return site_list
    site_list.sort(key=lambda i: datetime.strptime(i['bookingTime'], "%Y-%m-%dT%H:%M:%SZ"))
    earliest = datetime.strptime(site_list[0]['bookingTime'], "%Y-%m-%dT%H:%M:%SZ")
    furthest = datetime.strptime(site_list[len(site_list)-1]['bookingTime'], "%Y-%m-%dT%H:%M:%SZ")
    delta = earliest - furthest
    # print(delta)

    for item in site_list:
        b_point = datetime.strptime(item['bookingTime'],"%Y-%m-%dT%H:%M:%SZ")
        try:
            item['bookingTimeScore'] = (b_point - furthest) / delta * 100
        except ZeroDivisionError:
            item['bookingTimeScore'] = 100

        item['readableBookingTime'] = aslocaltimestr(b_point)
    return site_list


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)  # normalize might be unnecessary


def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%a, %d %b %Y, %H:%M')
    # return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')


def processing(ref_list, updated_list, booking_time_link):
    print(ref_list)
    available_site_list = create_eligible_list(ref_list, updated_list)
    print(available_site_list)
    available_site_list = request_booking_time(available_site_list, booking_time_link)
    available_site_list = calculate_time_score(available_site_list)
    available_site_list = available_site_list[0:10]
    print(available_site_list)

    return available_site_list
