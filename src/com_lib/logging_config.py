# -*- coding: utf-8 -*-
import logging
from pathlib import Path

from loguru import logger

# from settings import LOGURU_LOGGING_LEVEL
# from settings import LOGURU_RETENTION
# from settings import LOGURU_ROTATION
import settings


def config_log():
    # remove default logger
    # logger.remove()
    # set file path
    log_path = Path.cwd().joinpath("log").joinpath("app_log.log")
    # add new configuration
    logger.add(
        log_path,  # log file path
        level=settings.LOGURU_LOGGING_LEVEL.upper(),  # logging level
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",  # format of log
        enqueue=True,  # set to true for async or multiprocessing logging
        backtrace=False,  # turn to false if in production to prevent data leaking
        rotation=settings.LOGURU_ROTATION,  # file size to rotate
        retention=settings.LOGURU_RETENTION,  # how long a the logging data persists
        compression="zip",  # log rotation compression
        serialize=False,  # if you want it JSON style, set to true. But also change the format
    )

    # intercept standard logging
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    logging.basicConfig(
        handlers=[InterceptHandler()], level=settings.LOGURU_LOGGING_LEVEL.upper()
    )

