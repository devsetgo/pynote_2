# -*- coding: utf-8 -*-

import logging

import databases
from loguru import logger
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    pool,
    schema,
)

from settings import config_settings

engine = create_engine(
    config_settings.sqlalchemy_database_uri,
    poolclass=pool.QueuePool,
    max_overflow=10,
    pool_size=100,
)
metadata = MetaData()
database = databases.Database(config_settings.sqlalchemy_database_uri)


def create_db():

    metadata.create_all(engine)
    logger.info("Creating tables")


async def connect_db():
    await database.connect()
    logger.info("connecting to database")


async def disconnect_db():
    await database.disconnect()
    logger.info("disconnecting from database")


users = Table(
    "users",
    metadata,
    Column("user_id", String, primary_key=True),
    Column("user_name", String, index=True, unique=True),
    Column("password", String, index=True),
    Column("email", String, index=True),  # , unique=True),
    Column("first_name", String, index=True),
    Column("last_name", String, index=True),
    Column("address", String, index=True),
    Column("city", String, index=True),
    Column("state", String, index=True),
    Column("country", String, index=True),
    Column("postal", String, index=True),
    Column("phone", String, index=True),
    Column("mobile_phone", String, index=True),
    Column("is_active", Boolean, index=True),
    Column("is_admin", Boolean, index=True),
    Column("first_login", Boolean, index=True),
    Column("from_config", Boolean, index=True),
    Column("date_created", DateTime, index=True),
    Column("last_login", DateTime, index=True),
)

user_profiles = Table(
    "user_profiles",
    metadata,
    Column("id", String, index=True, primary_key=True),
    Column("user_id", String, index=True),
    Column("name", String, index=True),
    Column("link", String, index=True),
)

user_approval = Table(
    "user_approval",
    metadata,
    Column("access_id", String, index=True, primary_key=True),
    Column("date_created", DateTime, index=True),
    Column("date_updated", DateTime, index=True),
    Column("user_name", String, index=True),
    Column("is_reviewed", Boolean, index=True),
    Column("is_rejected", Boolean, index=True),
    Column("is_admin", Boolean, index=True),
)

user_login_failures = Table(
    "user_login_failures",
    metadata,
    Column("id", String, index=True, primary_key=True),
    Column("date_created", DateTime, index=True),
    Column("user_name", String, index=True),
    Column("ip_address", String, index=True),
)

notes = Table(
    "notes",
    metadata,
    Column("id", String, index=True, primary_key=True),
    Column("user_name", String(50), index=True, unique=True),
    Column("note", String(5000), index=True),
    Column("feeling", String(20), index=True),
    Column("word_count", Integer, index=True),
    Column("char_count", Integer, index=True),
    Column("sentiment_polarity", Float, index=True),
    Column("sentiment_subjectivity", Float, index=True),
    Column("date_created", DateTime),
    Column("date_updated", DateTime),
)

