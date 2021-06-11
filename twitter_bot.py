import tweet_bot_credential
# import schedule
import time
import tweepy
import random
import threading

WAIT_SECONDS = 900
counter = -0
import itertools



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
    alist = [0, 1, 2, 3, 4]

    combinations_object = itertools.combinations(alist, 2)
    combinations_list = list(combinations_object)
    # combinations_list = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    content = f"💉 Earliest vaccination dates\n\n"
    for item in combinations_list:
        if len(new_list[item[0]]['siteName'] + new_list[item[1]]['siteName']) <100:
            new = f"📍 {new_list[item[0]]['siteName']}\n🗓 {new_list[item[0]]['readableBookingTime']}\n\n"
            new += f"📍 {new_list[item[1]]['siteName']}\n🗓 {new_list[item[1]]['readableBookingTime']}\n\n"
            content = content + new
            break
    content += "Book here: https://tinyurl.com/ns-vax-book\n"
    # sample = list(range(0, len(new_list)))
    # random_seed = random.sample(sample, 2)
    # content = f"💉 Earliest vaccination dates\n\n"
    # for i in random_seed:
    #     new = f"📍 {new_list[i]['siteName']}\n🗓 {new_list[i]['readableBookingTime']}\n\n"
    #     content = content + new
    # content += "Book here: https://tinyurl.com/ns-vax-book\n"
    # content += "#NS #COVID19\n"
    # print(content)

    # for item in new_list:
    #     new = f"📍 {item['siteName']}\n🗓 {item['readableBookingTime']}\n\n"
    #     content = content + new
    # content += "Book here: https://novascotia.flow.canimmunize.ca/en/9874123-19-7418965?fbclid=IwAR0mx8GuTcL47-cqAEafer6xSHSAOZaedJcPx_n5XcDrSqWGn4MoxmMnC0c\n"
    # content += "#NS #COVID19\n"
    print(content)
    try:
        # api.update_status(content)
        print('> Content successfully posted on Twitter!')
    except tweepy.TweepError:
        print('Tweep Error:Status is a duplicate.')
        # print('> Content is successfully posted on Twitter!')
        print('> Posting function is suspended for 72 hours (as of 6pm, June 2021) !')
    except Exception as e:
        raise tweepy.TweepError(e)
    # except tweepy.TweepError:
    #     print('Tweep Error:Status is a duplicate.')

    threading.Timer(WAIT_SECONDS, create_tweet, args=(api, site_list)).start()


def create_bot(array, region_count):
    time.sleep(60)
    api = initialize_api()
    create_tweet(api, array)
