# -*- coding: utf-8 -*-
import datetime
import uuid

from loguru import logger

from core.crud_ops import execute_one_db, fetch_one_db
from core.db_setup import users


# register user
async def user_register(data: dict):
    """[summary]

    Arguments:
        data {dict} -- [description]

    Returns:
        [type] -- [description]
    """
    values = {
        # input fields
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "last_login": datetime.datetime.now(),
        "user_name": data["user_name"].lower(),
        "password": data["password"],
        "email": data["email"].lower(),
        # system created fields
        "user_id": str(uuid.uuid4()),
        "date_created": datetime.datetime.now(),
        "is_active": False,
        "is_admin": False,
    }
    logger.debug(values)
    query = users.insert()

    try:
        db_result = await execute_one_db(query=query, values=values)
        logger.debug(type(db_result))
    except Exception as e:
        logger.warning(f"An error occurred trying to update {user_name}")
        return "error"


# get user
async def user_info(user_name: str):
    """[summary]

    Arguments:
        user_name {str} -- [description]

    Returns:
        [type] -- [description]
    """
    query = users.select().where(users.c.user_name == user_name)
    logger.debug(query)

    try:

        result = await fetch_one_db(query=query)
        return result

    except Exception as e:
        logger.warning(f"An error occurred trying to update {user_name}")
        return "error"


# update user data
async def user_update(data: dict):
    """[summary]

    Arguments:
        data {dict} -- [description]
        data = {
            "first_name": str,
            "last_name": str,
            "email": str (valid email address),
            "user_name": exsiting user_name
            }
    """
    values = {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "last_login": datetime.datetime.now(),
        "email": data["email"].lower(),
    }
    user_name = data["user_name"]
    logger.debug(values)
    query = users.update().where(users.c.user_name == user_name)
    try:
        db_result = await execute_one_db(query=query, values=values)
        logger.debug(type(db_result))
        return "complete"
    except Exception as e:
        logger.warning(f"An error occurred trying to update {user_name}")
        return "error"


# update user login
async def user_login_update(user_name: dict):

    values: dict = {"last_login": datetime.datetime.now()}
    query = users.update().where(users.c.user_name == user_name)
    try:
        await execute_one_db(query=query, values=values)
        logger.info(f"{user_name} last login updated")
        return "complete"
    except Exception as e:
        logger.warning(f"An error occurred trying to update {user_name}")
        return "error"


# user active status
async def user_active_status(user_name: str, is_active: bool, is_admin: bool = None):
    """[summary]
        update  user status
    Arguments:
        user_id {str} -- [description]
        is_active {bool} -- [description]

    Keyword Arguments:
        is_admin {bool} -- [description] (default: {None})
    """
    if is_admin == None:
        is_admin = False
    values: dict = {"is_active": is_active, "is_admin": is_admin}
    query = users.update().where(users.c.user_name == user_name)
    try:
        await execute_one_db(query=query, values=values)
        logger.info(f"{user_name} status updated")
    except Exception as e:
        logger.warning(f"An error occurred trying to update {user_name}")
        return "error"
