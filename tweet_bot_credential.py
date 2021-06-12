import tweepy
import logging
import config
import facebook as fb

TWITTER_API_KEY= config.API_KEY
TWITTER_API_KEY_SECRET= config.KEY_SECRET
TWITTER_ACCESS_TOKEN= config.ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET= config.TWITTER_ACCESS_TOKEN_SECRET

FB_ACCESS_TOKEN = config.ACCESS_TOKEN_FB

logging.basicConfig(format='%(levelname)s [%(asctime)s] %(message)s', datefmt='%m/%d/%Y %r', level=logging.INFO)
logger = logging.getLogger()


def tw_create_api():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api_tw = tweepy.API(auth, wait_on_rate_limit=True)

    try:
        api_tw.verify_credentials()
    except Exception as e:
        logger.error('Authentication Error', exc_info=True)
        raise e
    logger.info(f"Authentication OK. Connected to @{api_tw.me().screen_name}")

    return api_tw


def fb_create_app():
    # The Graph API allows you to read and write data to and from the Facebook social graph
    api_fb = fb.GraphAPI(FB_ACCESS_TOKEN)

    return api_fb

