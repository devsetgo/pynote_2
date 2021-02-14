# -*- coding: utf-8 -*-
# import datetime
# import logging

# from loguru import logger
# from sqlalchemy.sql import and_

# from core.crud_ops import execute_one_db
# from core.crud_ops import fetch_all_db
# from core.crud_ops import fetch_one_db
# from core.db_setup import bots
# from core.db_setup import lyrics


# async def lyrics_for_bot(twitter_name: str):

#     logger.info(f"Fetching lyrics for {twitter_name}")
#     query = lyrics.select().where(lyrics.c.twitter_name == twitter_name)
#     logger.info(f"getting lyrics for {twitter_name}")
#     result = await fetch_all_db(query)
#     logging.debug(f"query result = {result}")
#     return result


# async def lyrics_remove(twitter_name: str):
#     """ Remove existing lyrics """
#     logger.info(f"Delete Lyrics for {twitter_name}")
#     query = lyrics.delete().where(lyrics.c.twitter_name == twitter_name.lower())
#     result = await fetch_one_db(query=query)
#     logging.debug(result)
#     return result


# async def bot_information(twitter_name: str):
#     """ Retrieve bot information """
#     query = bots.select().where(bots.c.twitter_name == twitter_name.lower())
#     result = await fetch_one_db(query)
#     logging.debug(f"bot data = {result}")
#     return result


# async def bot_delete(twitter_name: str):
#     """ Retrieve bot information """

#     delete_lyric = await lyrics_remove(twitter_name)

#     query = bots.delete().where(bots.c.twitter_name == twitter_name.lower())
#     result = await fetch_one_db(query)
#     logging.debug(f"bot data = {result}")
#     return result


# async def squence_one(twitter_name: str):
#     """ Increment by 1 the current sequence """
#     bot_data = await bot_information(twitter_name)
#     lyric_data = await lyrics_for_bot(twitter_name)

#     current_lyric_sequence = bot_data["current_lyric_sequence"]
#     if current_lyric_sequence >= len(lyric_data):
#         current_lyric_sequence = 1
#     else:
#         current_lyric_sequence += 1

#     logger.info(f"Increment Sequence by one for {twitter_name}")
#     query = bots.update().where(bots.c.twitter_name == twitter_name.lower())
#     values = {
#         "date_updated": datetime.datetime.now(),
#         "current_lyric_sequence": int(current_lyric_sequence),
#     }
#     result = await execute_one_db(query=query, values=values)
#     logging.debug(result)
#     logger.info(f"completed increment for {twitter_name}")
#     return result


# async def get_active_bots():

#     # get active bots
#     query = bots.select().where(bots.c.is_active == True)
#     logging.debug(f"query for bots: {query}")
#     result = await fetch_all_db(query)
#     logging.debug(f"LOOK AT THIS query result = {result}")
#     return result


# async def get_all_bots():

#     # get active bots
#     query = bots.select()
#     logging.debug(f"query for bots: {query}")
#     result = await fetch_all_db(query)
#     logging.debug(f"Query result = {result}")
#     return result


# async def get_current_lyric(current_sequence: int, twitter_name: str):

#     # get active bots
#     query = lyrics.select().where(
#         and_(
#             lyrics.c.twitter_name == twitter_name, lyrics.c.sequence == current_sequence
#         )
#     )
#     logging.debug(f"query for bots: {query}")
#     result = await fetch_one_db(query)
#     logging.debug(f"LOOK AT THIS query result = {result}")

#     return result


# async def get_lyrics_length(twitter_name: str):

#     """ return number of lyrics for bot """
#     # get active bots
#     query = lyrics.select().where(lyrics.c.twitter_name == twitter_name)
#     logging.debug(f"query for bots: {query}")
#     lyrics_list = await fetch_all_db(query)

#     result = len(lyrics_list)
#     logging.debug(f"Query result = {result}")
#     return result


# async def increment_one(twitter_name: str, current_lyric_sequence: int):

#     """ Increment by 1 the current sequence """
#     logger.info(f"Increment Sequence by one for {twitter_name}")
#     lyric_length = await get_lyrics_length(twitter_name)

#     logging.debug(lyric_length)

#     if lyric_length >= 1:

#         if current_lyric_sequence >= lyric_length:
#             new_sequence = 1
#         else:
#             new_sequence = current_lyric_sequence + 1

#         query = bots.update().where(bots.c.twitter_name == twitter_name)
#         values = {
#             "date_updated": datetime.datetime.now(),
#             "current_lyric_sequence": int(new_sequence),
#         }
#         await execute_one_db(query=query, values=values)
#         logger.info(f"completed increment for {twitter_name}")
#     else:
#         logger.info(f"Twitter Account {twitter_name} has no lyrics")
