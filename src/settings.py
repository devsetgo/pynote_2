# -*- coding: utf-8 -*-
"""Application configuration.
Most configuration is set via environment variables.
For local development, use a .env file to set
environment variables.
"""


# import os
import secrets
from functools import lru_cache

# from core.demo import create_demo_data

from pydantic import BaseSettings


class Settings(BaseSettings):
    # use_env = "dotenv"
    default_tags: list = ["Fun", "Life", "Work", "Unknown"]
    app_version: str = "1.0.0"
    release_env: str = "prd"
    https_on: bool = False
    prometheus_on: bool = True
    database_type: str = "sqlite"
    db_name: str = "sqlite_db/api.db"
    sqlalchemy_database_uri: str = "sqlite:///sqlite_db/api.db"
    workers: int = 2
    csrf_secret = secrets.token_urlsafe(64)
    secret_key = secrets.token_hex(64)
    invalid_character_list: list = [
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

    loguru_retention: str = "10 days"
    loguru_rotation: str = "100 MB"
    loguru_logging_level: str = "INFO"
    release_env: str = "prd"
    debug: bool = False
    sendgrid_key: str = "insert-key"
    login_timeout: int = 120
    admin_create: bool = False
    admin_user_name: str = None
    admin_user_key: str = None
    admin_user_email: str = None
    create_demo_data: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


config_settings = get_settings()
# config = Settings()
