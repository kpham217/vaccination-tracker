TWITTER_API_KEY="PyH1EDxN8aRvU7nZ2gGBfqkDG"
TWITTER_API_KEY_SECRET="WEZueY7AR585u1PaH2pgeBDoXBqUYSIevrVm5QxxdLVaU3YdB3"
TWITTER_ACCESS_TOKEN="1401205897699938308-NrjWBTHUWk5puJOcZJqjpr8g8M13NF"
TWITTER_ACCESS_TOKEN_SECRET="ORT2D6vLsURaW7fdAvI11whd3U69v2aVr0hAZMlBwSo9b"

import tweepy
import logging

logging.basicConfig(format='%(levelname)s [%(asctime)s] %(message)s', datefmt='%m/%d/%Y %r', level=logging.INFO)
logger = logging.getLogger()


def create_api():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error('Authentication Error', exc_info=True)
        raise e
    logger.info(f"Authentication OK. Connected to @{api.me().screen_name}")

    return api
