import tweet_bot_credential
import schedule
import time
import tweepy


counter = -1


def set_global():
    global counter
    counter += 1
    if counter == 3:
        counter = 0


def initialize_api():
    api = tweet_bot_credential.create_api()
    return api


def create_tweet(api, site_list):
    set_global()
    new_list = site_list[counter]
    print(str(counter)+'\n')
    print(new_list+'\n')
    new_list = new_list[0:2]
    content = f"💉 Earliest vaccination dates\n\n"
    for item in new_list:
        new = f"📍 {item['siteName']}\n🗓 {item['readableBookingTime']}\n\n"
        content = content + new

    print(content)
    try:
        api.update_status(content)
        print('> Content successfully posted on Twitter!')
    except tweepy.TweepError:
        print('Tweep Error:Status is a duplicate.')


def create_bot(array, region_count):
    time.sleep(240)
    # initiate()
    api = initialize_api()
    schedule.every(2).minutes.do(create_tweet, api=api, site_list=array)
    while True:
        schedule.run_pending()
        time.sleep(1)
