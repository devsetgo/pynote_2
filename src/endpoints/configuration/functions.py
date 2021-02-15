# -*- coding: utf-8 -*-
import datetime
import uuid

from loguru import logger
from endpoints.user import crud as user_crud
from core.crud_ops import execute_one_db, fetch_all_db, fetch_one_db
from core.db_setup import notes, tags
from endpoints.user import crud as user_crud
from sqlalchemy import and_


async def get_user_tags(user_name: str):
    user_data = await user_crud.user_info(user_name=user_name)
    query = notes.select()  # .where(notes.c.user_id == user_data['id'])
    try:
        results = await fetch_all_db(query=query)
        return results
    except Exception as e:
        logger.error(f"error: {e}")
