# -*- coding: utf-8 -*-
import datetime
import uuid

from loguru import logger
from sqlalchemy import and_

from core.crud_ops import execute_one_db, fetch_all_db, fetch_one_db
from core.db_setup import notes, tags
from core.sentiment import sentiment_check
from endpoints.user import crud as user_crud


# get notes for user
async def get_users_notes(user_id: str, limit: int = None, off_set: int = None):

    # set limit value if none
    if limit is None:
        limit: int = 20
    # set off_set value if none
    if off_set is None:
        off_set: int = 0

    # get user ID
    # user_data = await user_crud.user_info(user_name=user_name)
    query = (
        notes.select()
        .where(notes.c.user_id == user_id)
        .limit(limit)
        .offset(off_set)
        .order_by(notes.c.date_created.desc())
    )
    count_query = notes.select().where(notes.c.user_id == user_id)
    try:
        # query database
        db_results = await fetch_all_db(query=query)
        count_results = await fetch_all_db(query=count_query)
        # sort list by date_created in dictionary
        sorted_results = sorted(
            list(db_results), key=lambda k: k["date_created"], reverse=True
        )
        results: dict = {
            "config": {"off_set": off_set, "limit": limit, "qty": len(count_results)},
            "notes": db_results,
        }
        return results
    except Exception as e:
        logger.error(f"error: {e}")


async def get_note_id(user_id: str, note_id: str):

    # user_data = await user_crud.user_info(user_name=user_name)
    query = notes.select().where(
        and_(notes.c.user_id == user_id, notes.c.id == note_id)
    )
    try:
        results = await fetch_one_db(query=query)

        return results
    except Exception as e:
        logger.error(f"error: {e}")


async def get_users_tags(user_id: str):

    user_tags = await get_users_created_tags(user_id=user_id)
    global_tags = await get_global_tags()

    result: dict = {"user_tags": user_tags, "global_tags": global_tags}
    return result


async def get_users_created_tags(user_id: str):

    # user_data = await user_crud.user_info(user_id=user_id)
    query = (
        tags.select()
        .where(and_(tags.c.user_id == user_id, tags.c.is_active == True))
        .order_by(tags.c.default_value.desc())
    )
    try:
        results = await fetch_all_db(query=query)
        return results
    except Exception as e:
        logger.error(f"error: {e}")


async def get_global_tags():
    query = (
        tags.select()
        .where(and_(tags.c.cannot_delete == True, tags.c.is_active == True))
        .order_by(tags.c.default_value.desc())
    )
    try:
        results = await fetch_all_db(query=query)
        return results
    except Exception as e:
        logger.error(f"error: {e}")


async def add_new_note(data: dict, user_name: str):
    logger.critical(data)

    try:
        user_data = await user_crud.user_info(user_name=user_name)
    except Exception as e:
        logger.error(f"error: {e}")

    note = data["form_data"]["note"]
    sent = sentiment_check(text_str=note)
    query = notes.insert()
    dt = datetime.datetime.now()
    values: dict = {
        "id": str(uuid.uuid4()),
        "user_id": user_data["id"],
        "note": note.replace("\n", "<br>"),
        "preview": f"{note[0:30]}...",
        "tags": data["tags"],
        "mood": data["form_data"]["mood"],
        "word_count": len(note.strip().split(" ")),
        "char_count": len(note),
        "sentiment_polarity": sent.polarity,
        "sentiment_subjectivity": sent.subjectivity,
        "date_created": dt,
        "date_updated": dt,
        "created_year": dt.year,
        "created_month": dt.month,
        "created_day": dt.day,
    }
    try:
        await execute_one_db(query=query, values=values)
        return "new note complete"
    except Exception as e:
        logger.error(f"error: {e}")


async def update_note(data: dict, user_name: str):

    logger.debug(f"update note data:{data}")
    logger.debug(f"update note user_name:{user_name}")
    try:
        user_data = await user_crud.user_info(user_name=user_name)
    except Exception as e:
        logger.error(f"error: {e}")

    note = data["form_data"]["note"]

    sent = sentiment_check(text_str=note)
    query = notes.insert()
    values: dict = {
        "id": str(uuid.uuid4()),
        "user_id": user_data["id"],
        "note": note,
        "preview": f"{note[0:30]}...",
        "tags": data["tags"],
        "mood": data["form_data"]["mood"],
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


# get notes for user
async def get_search_notes(user_id: str, limit: int = None, off_set: int = None):

    # set limit value if none
    if limit is None:
        limit: int = 20
    # set off_set value if none
    if off_set is None:
        off_set: int = 0

    # get user ID
    # user_data = await user_crud.user_info(user_name=user_name)
    query = (
        notes.select()
        .where(notes.c.user_id == user_id)
        .limit(limit)
        .offset(off_set)
        .order_by(notes.c.date_created.desc())
    )
    count_query = notes.select().where(notes.c.user_id == user_id)
    try:
        # query database
        db_results = await fetch_all_db(query=query)
        count_results = await fetch_all_db(query=count_query)
        # sort list by date_created in dictionary
        sorted_results = sorted(
            list(db_results), key=lambda k: k["date_created"], reverse=True
        )
        results: dict = {
            "config": {"off_set": off_set, "limit": limit, "qty": len(count_results)},
            "notes": db_results,
        }
        return results
    except Exception as e:
        logger.error(f"error: {e}")
