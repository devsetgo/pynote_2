# -*- coding: utf-8 -*-

from loguru import logger
from datetime import datetime
from core import login_required
from resources import templates
from core.crud_ops import execute_one_db, fetch_all_db, fetch_one_db
from core.db_setup import notes, tags
from core.colors import HEX_COLORS, RGBa_COLORS
from devsetgo_lib.calendar_functions import get_month


async def get_metrics(user_id: str):
    query = (
        notes.select()
        .where(notes.c.user_id == user_id)
        .order_by(notes.c.date_created.desc())
    )
    logger.debug(f"user posts query: {query}")
    data = await fetch_all_db(query)
    logger.debug(f"Query result = {data}")
    colors = get_colors(12)
    results: dict = {
        "total_notes": len(data),
        "post_per_month": await posts_per_month(data=data),
        "post_per_year": await posts_per_year(data=data),
        "total_words": await total_words(data=data),
        "words_per_month": await words_per_month(data=data),
        "words_per_year": await words_per_year(data=data),
        "total_characters": await total_characters(data=data),
        "characters_per_month": await character_per_month(data=data),
        "characters_per_year": await character_per_year(data=data),
        "tag_count": 7,
        "mood_count": 7,
        "polarity_trend": 7,
        "subjectivity_trend": 7,
        "hex": HEX_COLORS,
        "rgba": RGBa_COLORS,
    }
    logger.debug(results)
    print(results["post_per_year"])
    return results


def get_colors(length: int):
    return {"hex": HEX_COLORS[:length], "rgba": RGBa_COLORS[:length]}


async def posts_per_month(data: list):

    results: dict = {}
    for d in data:
        year = str(d["created_year"])
        month = get_month(d["created_month"])

        if year not in results:
            year_dict: dict = {
                "January": 0,
                "February": 0,
                "March": 0,
                "April": 0,
                "May": 0,
                "June": 0,
                "July": 0,
                "August": 0,
                "September": 0,
                "October": 0,
                "November": 0,
                "December": 0,
            }
            results[year] = year_dict
            results[year][month] = 1

        if year in results:
            results[year][month] = results[year][month] + 1

    result_dict: dict = {}
    years: list = []
    months_list: list = []
    for k, v in results.items():
        years.append(v)
        month_data: list = []

        for a, b in v.items():
            month_data.append(b)

        months_list.append(month_data)

    result_dict: dict = {
        "years": years,
        "months": months_list,
        "qty_years": len(years),
    }
    return result_dict


async def posts_per_year(data: list):
    data_dict: dict = {}

    for d in data:
        year = str(d["created_year"])

        if year not in data_dict:
            data_dict[year] = 1
        else:
            data_dict[year] += 1

    results: dict = {
        "years": list(data_dict.keys()),
        "data": list(data_dict.values()),
        "qty": len(list(data_dict.keys())),
    }
    return results


async def total_characters(data: list):
    counts: list = []
    for d in data:
        counts.append(d["char_count"])
    results: int = sum(counts)
    return results


async def total_words(data: list):
    counts: list = []
    for d in data:
        counts.append(d["word_count"])
    results: int = sum(counts)
    return results


async def character_per_month(data: list):
    results: dict = {}
    for d in data:
        year = str(d["created_year"])
        month = get_month(d["created_month"])

        if year not in results:
            year_dict: dict = {
                "January": 0,
                "February": 0,
                "March": 0,
                "April": 0,
                "May": 0,
                "June": 0,
                "July": 0,
                "August": 0,
                "September": 0,
                "October": 0,
                "November": 0,
                "December": 0,
            }
            results[year] = year_dict
            results[year][month] = d["char_count"]

        if year in results:
            results[year][month] = results[year][month] + d["char_count"]
    return results


async def words_per_month(data: list):
    results: dict = {}
    for d in data:
        year = str(d["created_year"])
        month = get_month(d["created_month"])

        if year not in results:
            year_dict: dict = {
                "January": 0,
                "February": 0,
                "March": 0,
                "April": 0,
                "May": 0,
                "June": 0,
                "July": 0,
                "August": 0,
                "September": 0,
                "October": 0,
                "November": 0,
                "December": 0,
            }
            results[year] = year_dict
            results[year][month] = d["word_count"]

        if year in results:
            results[year][month] = results[year][month] + d["word_count"]
    return results


async def character_per_year(data: list):
    results: dict = {}
    for d in data:
        year = str(d["created_year"])

        if year not in results:
            results[year] = d["char_count"]
        else:
            results[year] += d["char_count"]
    return results


async def words_per_year(data: list):
    results: dict = {}
    for d in data:
        year = str(d["created_year"])

        if year not in results:
            results[year] = d["word_count"]
        else:
            results[year] += d["word_count"]
    return results


async def tags_count(data: list):
    pass


async def mood_trends(data: list):
    pass


async def polarity_trend(user_id: str):
    pass


async def subjectivity_trend(user_id: str):
    pass


async def mood_per_month(user_id: str):
    pass
