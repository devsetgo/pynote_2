# -*- coding: utf-8 -*-
import datetime
import logging
import uuid

from loguru import logger
from sqlalchemy.sql import and_

from app_functions.crud_ops import execute_one_db
from app_functions.crud_ops import fetch_all_db
from app_functions.crud_ops import fetch_one_db
from app_functions.db_setup import notes


# get notes for user
async def users_notes(user_name:str):

    query=notes.select().where(notes.c.user_name==user_name)
    results = await fetch_all_db(query=query)
    return results
