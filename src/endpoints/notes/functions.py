# -*- coding: utf-8 -*-
import datetime
import uuid

from loguru import logger
from textblob import TextBlob

from core.crud_ops import execute_one_db, fetch_all_db
from core.db_setup import notes
from endpoints.user import crud as user_crud
from sqlalchemy import and_

# get notes for user
async def get_users_notes(user_name: str):
    user_data = await user_crud.user_info(user_name=user_name)
    query = notes.select()  # .where(notes.c.user_id == user_data['id'])
    results = await fetch_all_db(query=query)
    logger.critical(f"HERE {results}")
    return results


async def get_note_id(user_name: str,note_id:str):

    user_data = await user_crud.user_info(user_name=user_name)
    query = notes.select().where(and_(notes.c.user_id == user_data['id'], notes.c.id == note_id))
    results = await fetch_all_db(query=query)
    logger.critical(f"HERE {results}")
    return results


async def get_users_tags(user_name: str):
    return "x"

async def add_new_note(data: dict, user_name: str):
    logger.critical(data)
    user_data = await user_crud.user_info(user_name=user_name)

    note = data["form_data"]["note"]
    sent = sentiment_check(text_str=note)
    query = notes.insert()
    values: dict = {
        "id": str(uuid.uuid4()),
        "user_id": user_data["id"],
        "note": note,
        "preview": note[0:100],
        "tags": data["tags"],
        "mood": data["form_data"]["mood"],
        "word_count": len(note.strip().split(" ")),
        "char_count": len(note),
        "sentiment_polarity": sent.polarity,
        "sentiment_subjectivity": sent.subjectivity,
        "date_created": datetime.datetime.now(),
        "date_updated": datetime.datetime.now(),
    }
    await execute_one_db(query=query, values=values)
    return "new note complete"


def sentiment_check(text_str: str):
    data = TextBlob(text_str)
    result = data.sentiment
    return result
