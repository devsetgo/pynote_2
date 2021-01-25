# -*- coding: utf-8 -*-

import logging

import databases
from sqlalchemy import Column, Table,String,Boolean, DateTime,Date,Integer,Float,ForeignKey,Text,create_engine,pool,MetaData,schema
from loguru import logger

from settings import SQLALCHEMY_DATABASE_URI

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    poolclass=pool.QueuePool,
    max_overflow=10,
    pool_size=100,
)
metadata = MetaData()
database = databases.Database(SQLALCHEMY_DATABASE_URI)


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
    Column("email", String, index=True), #, unique=True),
    Column("first_name", String, index=True),
    Column("last_name", String, index=True),
    Column("is_active", Boolean, index=True),
    Column("is_admin", Boolean, index=True),
    Column("first_login", Boolean, index=True),
    Column("from_config", Boolean, index=True),
    Column("date_created", DateTime, index=True),
    Column("last_login", DateTime, index=True),
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

# ItemDetail = Table('ItemDetail',
#     Column('id', Integer, primary_key=True),
#     Column('itemId', Integer, ForeignKey('Item.id')),
#     Column('detailId', Integer, ForeignKey('Detail.id')),
#     Column('endDate', Date))

# class Item(Base):
#     __tablename__ = 'Item'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255))
#     description = Column(Text)
#     details = relationship('Detail', secondary=ItemDetail, backref='Item')

# class Detail(Base):
#     __tablename__ = 'Detail'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     value = Column(String)
#     items = relationship('Item', secondary=ItemDetail, backref='Detail')

# bots = Table(
#     "bots",
#     metadata,
#     Column("bot_id", String, primary_key=True),
#     Column("created_by", String, index=True),
#     Column("bot_type", String),
#     Column("bot_group", String),
#     Column("twitter_name", String, unique=True),
#     Column("image_name", String, index=True),
#     Column("consumer_key", String, index=True),
#     Column("consumer_secret", String, index=True),
#     Column("access_token", String, index=True),
#     Column("access_token_secret", String, index=True),
#     Column("description", String, index=True),
#     Column("is_active", Boolean, index=True),
#     Column("date_created", DateTime, index=True),
#     Column("date_updated", DateTime, index=True),
#     Column("current_lyric_sequence", Integer, index=True),
# )

# lyrics = Table(
#     "lyrics",
#     metadata,
#     Column("pk", Integer, primary_key=True),
#     Column("twitter_name", String, index=True),
#     Column("lyric_line", String, index=True),
#     Column("sequence", Integer, index=True),
#     Column("is_active", Boolean),
#     Column("date_created", DateTime),
#     Column("date_updated", DateTime),
# )
