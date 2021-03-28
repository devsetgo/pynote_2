# -*- coding: utf-8 -*-
"""
database simple functions. Pass query and where needed values and get result back
"""


from loguru import logger

from core.db_setup import database


async def fetch_one_db(query):
    try:
        logger.debug(f"running query {query}")
        result = await database.fetch_one(query=query)
        logger.debug(str(result))
        return result
    except Exception as e:
        logger.critical(f"error: {e}")
        return e


async def fetch_all_db(query):
    try:
        logger.debug(f"running query {query}")
        result = await database.fetch_all(query=query)
        logger.debug(str(result))
        return result
    except Exception as e:
        logger.critical(f"error: {e}")
        return e


async def execute_one_db(query, values: dict = None):

    try:
        logger.debug(f"running query {query}")
        await database.execute(query=query, values=values)
        result = "complete"
        logger.debug(str(result))
        return result
    except Exception as e:
        logger.critical(f"error: {e}")
        return e


async def execute_many_db(query, values: list):
    try:
        logger.debug(f"running query {query}")
        await database.execute_many(query=query, values=values)
        result = "complete"
        logger.debug(str(result))
        return result
    except Exception as e:
        logger.critical(f"error: {e}")
        return e
