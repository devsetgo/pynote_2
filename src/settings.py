# -*- coding: utf-8 -*-
"""Application configuration.
Most configuration is set via environment variables.
For local development, use a .env file to set
environment variables.
"""
import logging
import os
import secrets

from loguru import logger
from starlette.config import Config

# get environment variables
config = Config(".env")
USE_ENV = config("USE_ENV", default="docker")

CSRF_SECRET = secrets.token_urlsafe(64)
SECRET_KEY = secrets.token_hex(64)
INVALID_CHARACTER_LIST: list = [
    " ",
    ";",
    "<",
    ">",
    "/",
    "\\",
    "{",
    "}",
    "[",
    "]",
    "+",
    "=",
    "?",
    "&",
    "," ":",
    "'",
    ".",
    '"',
    "`",
]


# Application information
if USE_ENV.lower() == "dotenv":
    logger.info("external configuration is for use with {USE_ENV.lower()}")
    # dotenv variables
    APP_VERSION = config("APP_VERSION", default="1.0.0")
    # Application Configurations
    SQLALCHEMY_DATABASE_URI = config(
        "SQLALCHEMY_DATABASE_URI", default="sqlite:///sqlite_db/starlette_ui.db"
    )
    # set release environment settings
    RELEASE_ENV = config("RELEASE_ENV", default="prd")

    # Safety check to prevent debug mode or mocking in production
    if RELEASE_ENV == "prd":
        DEBUG = False
    else:
        DEBUG = config("DEBUG", default=False)

    # Sendgrid
    SENDGRID_API_KEY = config("SENDGRID_API_KEY", default="none")
    #security config
    LOGIN_TIMEOUT = int(config("LOGIN_TIMEOUT", default=120))
    # LOGIN_TIMEOUT=int(LOGIN_TIMEOUT)

    # Loguru settings
    LOGURU_RETENTION = config("LOGURU_RETENTION", default="10 days")
    LOGURU_ROTATION = config("LOGURU_ROTATION", default="100 MB")
    LOGURU_LOGGING_LEVEL = config("LOGURU_LOGGING_LEVEL", default="INFO")
    ADMIN_CREATE = config("ADMIN_CREATE", default="False")
    ADMIN_USER_NAME = config("ADMIN_USER_NAME", default=None)
    ADMIN_USER_KEY = config("ADMIN_USER_KEY", default=None)
    ADMIN_USER_EMAIL = config("ADMIN_USER_EMAIL",default=None)
else:
    logger.info(f"external configuration is for use with {USE_ENV.lower()}")
    # docker variables
    APP_VERSION = os.environ["APP_VERSION"]
    # Application Configurations
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    # set release environment settings
    RELEASE_ENV = os.environ["RELEASE_ENV"]
    # Safety check to prevent debug mode or mocking in production
    if RELEASE_ENV == "prd":
        DEBUG = False
    else:
        DEBUG = os.environ["DEBUG"]

    # Sendgrid
    SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
    #security config
    LOGIN_TIMEOUT = config("LOGIN_TIMEOUT", default=120)
    if LOGIN_TIMEOUT is None:
        LOGIN_TIMEOUT = 120
    else:
        LOGIN_TIMEOUT = int(LOGIN_TIMEOUT)
    # Loguru settings
    #LOGURU_RETENTION = config("LOGURU_RETENTION", default="10 days")
    #     LOGURU_ROTATION = config("LOGURU_ROTATION", default="10 MB")
    # LOGURU_LOGGING_LEVEL = config("LOGURU_LOGGING_LEVEL", default="WARNING")
    LOGURU_RETENTION = os.environ["LOGURU_RETENTION"]
    if LOGURU_RETENTION is None:
        LOGURU_RETENTION = "10 days"
    
    LOGURU_ROTATION = os.environ["LOGURU_ROTATION"]
    if LOGURU_ROTATION is None:
        LOGURU_ROTATION = "100 MB"
    
    LOGURU_LOGGING_LEVEL = os.environ["LOGURU_LOGGING_LEVEL"]
    if LOGURU_LOGGING_LEVEL is None:
        LOGURU_LOGGING_LEVEL = "INFO"
    
    ADMIN_CREATE = os.environ["ADMIN_CREATE"]
    if ADMIN_CREATE.lower()==None:
        ADMIN_CREATE=False

    ADMIN_USER_NAME = os.environ["ADMIN_USER_NAME"]
    ADMIN_USER_KEY = os.environ["ADMIN_USER_KEY"]
    ADMIN_USER_EMAIL=os.environ["ADMIN_USER_EMAIL"]