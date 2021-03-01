# -*- coding: utf-8 -*-
import datetime
import time
import uuid
import random
from loguru import logger
from sqlalchemy import and_
from textblob import TextBlob
import silly
from core.crud_ops import execute_one_db, fetch_all_db, fetch_one_db
from core.db_setup import notes, tags, users
from endpoints.user import crud as user_crud
from endpoints.notes.forms import MOODS
from settings import config_settings


async def create_demo_data():
    logger.warning("create demo data set to true")
    query=users.select().where(users.c.is_admin==True)
    user_data=await fetch_one_db(query=query)

    note_query=notes.select()
    note_data=await fetch_one_db(query=note_query)

    if note_data is None:
        logger.warning("creating demo data")
        for t in range(0,300):
            time.sleep(.01)
            logger.info(f"creating demo data #{t}")
            await create_demo_notes(user_id=user_data['id'])


async def create_demo_notes(user_id: str):

    note = silly.paragraph(length=random.randint(1, 6))
    sent = sentiment_check(text_str=note)
    query = notes.insert()
    values: dict = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "note": note.replace("\n", "<br>"),
        "preview": f"{note[0:30]}...",
        "tags": rand_tags(),
        "mood": rand_mood(),
        "word_count": len(note.strip().split(" ")),
        "char_count": len(note),
        "sentiment_polarity": sent.polarity,
        "sentiment_subjectivity": sent.subjectivity,
        "date_created": random_date(),
        "date_updated": datetime.datetime.now(),
    }
    
    try:
        await execute_one_db(query=query, values=values)
        return "new note complete"
    except Exception as e:
        logger.error(f"error: {e}")


def random_date():
    r=random.randint(0,3000)
    now=datetime.datetime.now()
    delta=datetime.timedelta(r)
    return now - delta

def sentiment_check(text_str: str):
    data = TextBlob(text_str)
    result = data.sentiment
    return result


def rand_mood():
    result = MOODS[random.randint(0,len(MOODS) - 1)]
    return result


def rand_tags():
    tags:list=[{'Life': 'on'}, {'Fun': 'on'}, {'Work': 'on'}, {'Unknown': 'on'}]
    r=random.randint(1,3)
    result=[]
    
    # result=tags[random.randint(len(tags)-1)]
    return tags


async def get_admin_account() -> str:
    query = users.select().where(users.c.is_admin == True)
    result = await fetch_one_db(query=query)
    return result["id"]
