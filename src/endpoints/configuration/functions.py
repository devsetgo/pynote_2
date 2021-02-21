# -*- coding: utf-8 -*-
import datetime
import uuid

from loguru import logger
from sqlalchemy import and_

from core.crud_ops import execute_one_db, fetch_all_db, fetch_one_db
from core.db_setup import tags


async def get_user_tags(user_id: str):
    # user_data = await user_crud.user_info(user_name=user_name)
    query = tags.select().where(tags.c.user_id == user_id)
    try:
        results = await fetch_all_db(query=query)
        return results
    except Exception as e:
        logger.error(f"error: {e}")


async def check_dup_tag(tag: str, user_id: str) -> bool:

    query = tags.select().where(
        and_(tags.c.user_id == user_id, tags.c.name == tag.capitalize())
    )
    try:
        results = await fetch_one_db(query=query)

        if results == None:
            return False
        else:
            return True

    except Exception as e:
        logger.error(f"error: {e}")


async def add_new_tag(form_data: dict, user_id: str) -> str:
    # check if duplicate
    # add Tag
    # confirm
    # if error
    # check if duplicate
    is_dup: bool = await check_dup_tag(tag=form_data["name"], user_id=user_id)
    logger.debug(f"is_dup value: {is_dup}")

    if is_dup == False:
        logger.info(f"{form_data['name']} for {user_id} IS NOT a duplicate")

        if "default_value" not in form_data:
            default_value = False
        else:
            default_value = True

        if "is_active" not in form_data:
            is_active = False
        else:
            is_active = True

        values: dict = {
            "id": str(uuid.uuid4()),
            "name": form_data["name"].capitalize(),
            "user_id": user_id,
            "default_value": default_value,
            "is_active": is_active,
            "cannot_delete": False,
            "date_created": datetime.datetime.now(),
            "date_updated": datetime.datetime.now(),
        }
        query = tags.insert()
        try:
            await execute_one_db(query=query, values=values)
            return "complete"
        except Exception as e:
            logger.error(f"error: {e}")

    else:
        logger.info(f"{form_data['name']} for {user_id} IS a duplicate")
        return "is duplicate"
