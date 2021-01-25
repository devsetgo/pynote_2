# # -*- coding: utf-8 -*-
# import logging

# from loguru import logger

# from app_functions.crud_ops import fetch_one_db
# from app_functions.db_setup import bots

# # async def botname_check(bot_name: str):

# #     # check if unique user_name
# #     query = bots.select().where(bots.c.bot_name == bot_name.lower())
# #     logger.info(f"validating user_name: {bot_name}")
# #     result = await fetch_one_db(query)
# #     logging.debug(f"LOOK AT THIS query result = {result}")
# #     return result


# async def twittername_check(twitter_name: str):

#     # check if unique email
#     query = bots.select().where(bots.c.twitter_name == twitter_name.lower())
#     logger.info(f"validating email: {twitter_name}")
#     result = await fetch_one_db(query)
#     logging.debug(f"query result = {result}")
#     return result


# # bot_id Integer
# # bot_name String
# # twitter_name String
# # consumer_key String
# # consumer_secret String
# # access_token String
# # access_token_secret String
# # description String
# # is_active Boolean
# # date_create DateTime
