# -*- coding: utf-8 -*-
import datetime
import uuid
import random
from loguru import logger
from sqlalchemy import and_
from textblob import TextBlob
import silly
from core.crud_ops import execute_one_db, fetch_all_db, fetch_one_db
from core.db_setup import notes, tags
from endpoints.user import crud as user_crud
from endpoints.note.forms import MOODS
from resource import DEFAULT_TAGS

async def create_demo_notes(qty:int):
    note=silly.paragraph(length=5)
    sent = sentiment_check(text_str=note)
    
    query = notes.insert()
    values: dict = {
        "id": str(uuid.uuid4()),
        "user_id": user_data["id"],
        "note": note.replace("\n", "<br>"),
        "preview": f"{note[0:30]}...",
        "tags": data["tags"],
        "mood": rand_mood(),
        "word_count": len(note.strip().split(" ")),
        "char_count": len(note),
        "sentiment_polarity": sent.polarity,
        "sentiment_subjectivity": sent.subjectivity,
        "date_created": datetime.datetime.now(),
        "date_updated": datetime.datetime.now(),
    }
    try:
        await execute_one_db(query=query, values=values)
        return "new note complete"
    except Exception as e:
        logger.error(f"error: {e}")

def sentiment_check(text_str: str):
    data = TextBlob(text_str)
    result = data.sentiment
    return result

def rand_mood():
    return MOODS[random.randint(len(MOODS)-1)]

def rand_tags():
    result:dict={"tags":[random.randint(len(DEFAULT_TAGS)-1)]}
    return DEFAULT_TAGS