# -*- coding: utf-8 -*-
import asyncio
import datetime
import logging
import uuid

from loguru import logger
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from core import db_setup
from core.crud_ops import execute_one_db, fetch_all_db, fetch_one_db
from core.db_setup import create_db, tags, users
from core.demo import create_demo_data
from core.logging_config import config_log
from core.pass_lib import encrypt_pass
from settings import config_settings


# templates and static files
templates = Jinja2Templates(directory="templates")
statics = StaticFiles(directory="statics")

DEFAULT_TAGS: list = config_settings.default_tags


def init_app():

    config_log()
    logger.info("Initiating application")

    create_db()
    logging.info("Initiating database-standard logging")


async def startup():

    logger.info("starting up services")
    await db_setup.connect_db()

    await create_admin()
    await add_default_tags()


async def shutdown():

    logger.info("shutting down services")
    await db_setup.disconnect_db()


async def add_default_tags():
    check_query = tags.select()
    check_result = await fetch_all_db(query=check_query)
    logger.debug(str(check_result))

    for t in DEFAULT_TAGS:
        check_query = tags.select().where(tags.c.name == t)
        check_result = await fetch_one_db(query=check_query)

        if check_result is None:
            if t == "Life":
                default_value = True
            else:
                default_value = False
            values: dict = {
                "id": str(uuid.uuid4()),
                "name": t.capitalize(),
                "is_active": True,
                "cannot_delete": True,
                "default_value": default_value,
                "date_created": datetime.datetime.now(),
                "date_updated": datetime.datetime.now(),
            }
            query = tags.insert()
            logging.info(f"Creating tag {t}")
            try:
                db_result = await execute_one_db(query=query, values=values)
                logging.debug(type(db_result))
                logging.warning(f"adding tag '{t}'")
            except Exception as e:
                logger.warning(f"An error occurred trying to update {t}")
                return "error"
    # Column("id", String, index=True, primary_key=True),
    # Column("name", String(50), index=True),
    # Column("user_id", String(50), index=True),
    # Column("is_active", Boolean, index=True),
    # Column("cannot_delete", Boolean, index=True),
    # Column("date_created", DateTime),
    # Column("date_updated", DateTime),


async def create_admin():

    await asyncio.sleep(0.5)

    if config_settings.admin_create == True:
        user_id = str(uuid.uuid4())
        check_query = users.select()
        check_result = await fetch_all_db(query=check_query)
        logger.debug(str(check_result))

        if len(check_result) == 0:

            hashed_pwd = encrypt_pass(config_settings.admin_user_key)
            values = {
                # input fields
                "first_name": "admin",
                "last_name": "istrator",
                "last_login": datetime.datetime.now(),
                "user_name": config_settings.admin_user_name.lower(),
                "password": hashed_pwd,
                "email": config_settings.admin_user_email,
                "address": "123 Maple St",
                "city": "Clearwater",
                "state": "Florida",
                "country": "USA",
                "postal": "33761",
                "phone": "727-456-7890",
                "mobile_phone": "727-456-7890",
                # system created fields
                "id": user_id,
                "date_created": datetime.datetime.now(),
                "is_active": True,
                "is_admin": True,
                "from_config": True,
                "first_login": True,
            }
            logging.debug(values)
            query = users.insert()
            logging.warning("Creating Admin account")
            try:
                db_result = await execute_one_db(query=query, values=values)
                logging.debug(type(db_result))
            except Exception as e:
                logger.warning(
                    f"An error occurred trying to update {config_settings.admin_user_name.lower()}"
                )
                return "error"

        else:
            logger.warning(
                "Skipping first account setup as there are existing users. DISABLE create ADMIN_CREATE for security."
            )

    if config_settings.create_demo_data == True:
        import time

        time.sleep(0.5)
        await create_demo_data()
