import tweet_bot_credential
import schedule
import time


def initialize_api():
    api = tweet_bot_credential.create_api()
    return api


def create_tweet(api, site_list):
    site_list = site_list[0:2]
    content = f"💉 Earliest vaccination dates\n\n"
    for item in site_list:
        new = f"📍 {item['siteName']}\n🗓 {item['readableBookingTime']}\n\n"
        content = content + new

    print(content)
    api.update_status(content)
    print('> Content posted on Twitter!')


def set_order(region_count, counter):
    counter += 1
    if counter == region_count:
        counter = 0
    return counter


def create_bot(array, region_count):
    time.sleep(120)
    counter = 0
    api = initialize_api()
    schedule.every(2).minutes.do(create_tweet, api=api, site_list=array[set_order(region_count, counter)])
    while True:
        schedule.run_pending()
        time.sleep(1)
