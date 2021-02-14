# -*- coding: utf-8 -*-
import logging

import tweepy
from loguru import logger


def tweet_this(bot_data: dict, tweet_data: str):

    logging.debug(bot_data["consumer_key"])
    logging.debug(tweet_data["lyric_line"])
    # authentication
    auth = tweepy.OAuthHandler(bot_data["consumer_key"], bot_data["consumer_secret"])
    auth.set_access_token(bot_data["access_token"], bot_data["access_token_secret"])

    # Creation of the actual interface, using authentication
    # api = tweepy.API(auth)
    # Sample method, used to update a status

    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)
    # Send Tweet to Twitter
    api.update_status(tweet_data["lyric_line"])
    logger.warning(
        f'send to @{bot_data["twitter_name"]} this Tweet: {tweet_data["lyric_line"]}'
    )
