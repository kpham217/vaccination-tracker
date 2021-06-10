import tweet_bot_credential
# import schedule
import time
import tweepy
import random
import threading

WAIT_SECONDS = 900
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
    sample = list(range(0, len(new_list)))
    random_seed = random.sample(sample, 2)
    content = f"💉 Earliest vaccination dates\n\n"
    for i in random_seed:
        new = f"📍 {new_list[i]['siteName']}\n🗓 {new_list[i]['readableBookingTime']}\n\n"
        content = content + new
    content += "Book here: https://tinyurl.com/ns-vax-book\n"
    content += "#NS #COVID19\n"
    print(content)
    try:
        api.update_status(content)
        print('> Content successfully posted on Twitter!')
    except Exception as e:
        raise tweepy.TweepError(e)
    # except tweepy.TweepError:
    #     print('Tweep Error:Status is a duplicate.')

    threading.Timer(WAIT_SECONDS, create_tweet, args=(api, site_list)).start()


def create_bot(array, region_count):
    time.sleep(60)
    api = initialize_api()
    create_tweet(api, array)
