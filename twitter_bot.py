import tweet_bot_credential
# import schedule
import time
import tweepy
import random
import threading
import itertools


WAIT_SECONDS = 1800
counter = 0


def set_global(region_count):
    global counter
    counter += 1
    if counter == region_count:
        counter = 0


def initialize_api():
    # api_tw = tweet_bot_credential.tw_create_api()
    api_fb = tweet_bot_credential.fb_create_app()
    api_tw =1
    # api_fb=1
    return api_tw, api_fb


def create_tweet(api_tw, api_fb, site_list,region_count):
    set_global(region_count)
    new_list = site_list[counter]
    # alist = [0, 1, 2, 3, 4]
    if new_list:
        # combinations_object = itertools.combinations(alist, 2)
        # combinations_list = list(combinations_object)
        # # combinations_list = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
        # content = f"💉 Earliest vaccination dates\n\n"
        # for item in combinations_list:
        #     if len(new_list[item[0]]['siteName'] + new_list[item[1]]['siteName']) <100:
        #         new = f"📍 {new_list[item[0]]['siteName']}\n🗓 {new_list[item[0]]['readableBookingTime']}\n\n"
        #         new += f"📍 {new_list[item[1]]['siteName']}\n🗓 {new_list[item[1]]['readableBookingTime']}\n\n"
        #         content = content + new
        #         break
        # content += "Book here: https://tinyurl.com/ns-vax-book\n"

        if len(new_list) == 1:
            content = f"💉 Earliest vaccination dates\n\n"
            new = f"📍 {new_list[0]['siteName']}\n🗓 {new_list[0]['readableBookingTime']}\n\n"
            content = content + new
            content += "Book here: https://tinyurl.com/ns-vax-book\n"
            content += "#NS #COVID19\n"
        else:
            sample = list(range(0, len(new_list)))
            random_seed = random.sample(sample, 2)
            content = f"💉 Earliest vaccination dates\n\n"
            for i in random_seed:
                new = f"📍 {new_list[i]['siteName']}\n🗓 {new_list[i]['readableBookingTime']}\n\n"
                content = content + new
            content += "Book here: https://tinyurl.com/ns-vax-book\n"
            # content += "#NS #COVID19\n"



        # for item in new_list:
        #     new = f"📍 {item['siteName']}\n🗓 {item['readableBookingTime']}\n\n"
        #     content = content + new
        # content += "Book here: https://novascotia.flow.canimmunize.ca/en/9874123-19-7418965?fbclid=IwAR0mx8GuTcL47-cqAEafer6xSHSAOZaedJcPx_n5XcDrSqWGn4MoxmMnC0c\n"
        # content += "#NS #COVID19\n"
        print(content)
        try:
            # [Twitter] Post a Tweet on Twitter
            # api.update_status(content)
            # print('> Content successfully posted on Twitter!')
            print('> Posting function is suspended for 72 hours (as of 6pm, June 2021) !')

            # [Facebook] Post a message in the facebook page
            api_fb.put_object("me", "feed", message=content)
            print('> Content successfully posted on FaceBook!')

        except Exception as e:
            raise e
            # raise tweepy.TweepError(e)


    threading.Timer(WAIT_SECONDS, create_tweet, args=(api_tw, api_fb, site_list, region_count)).start()


def create_bot(array, region_count):
    time.sleep(60)
    api_tw, api_fb = initialize_api()
    create_tweet(api_tw, api_fb, array, region_count)
