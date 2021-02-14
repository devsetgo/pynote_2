# -*- coding: utf-8 -*-
import datetime
import logging
import uuid

from loguru import logger
from sqlalchemy.sql import and_

from app_functions.crud_ops import execute_one_db, fetch_all_db, fetch_one_db
from app_functions.db_setup import notes
from endpoints.user import crud as user_crud

# get notes for user
async def users_notes(user_name: str):
    user_data = await user_crud.user_info(user_name=user_name)
    query = notes.select()  # .where(notes.c.user_id == user_data['id'])
    results = await fetch_all_db(query=query)
    logger.critical(f"HERE {results}")
    return results


async def add_new_note(data: dict, user_name: str):
    logger.critical(data)
    user_data = await user_crud.user_info(user_name=user_name)

    query = notes.insert()
    values: dict = {
        "id": str(uuid.uuid4()),
        "user_id": user_data["id"],
        "note": data["form_data"]["note"],
        "tags": data["tags"],
        "mood": data["form_data"]["mood"],
        "word_count": 1,
        "char_count": 1,
        "sentiment_polarity": 1,
        "sentiment_subjectivity": 1.1,
        "date_created": datetime.datetime.utcnow(),
        "date_updated": datetime.datetime.utcnow(),
    }
    await execute_one_db(query=query, values=values)
    return "new note complete"

    # Column("id", String, index=True, primary_key=True),
    # Column("user_name", String(50), index=True, unique=True),
    # Column("note", String(5000), index=True),
    # Column("tags", JSON()),
    # Column("feeling", String(20), index=True),
    # Column("word_count", Integer, index=True),
    # Column("char_count", Integer, index=True),
    # Column("sentiment_polarity", Float, index=True),
    # Column("sentiment_subjectivity", Float, index=True),
    # Column("date_created", DateTime),
    # Column("date_updated", DateTime),
