# -*- coding: utf-8 -*-

from loguru import logger
from datetime import datetime
from core import login_required
from resources import templates
from core.crud_ops import execute_one_db, fetch_all_db, fetch_one_db
from core.db_setup import notes, tags


async def get_metrics(user_id: str):
    query = notes.select().where(notes.c.user_id == user_id)
    logger.debug(f"user posts query: {query}")
    data = await fetch_all_db(query)
    logger.debug(f"Query result = {data}")

    results: dict = {
        "total_notes": len(data),
        "post_per_month": await posts_per_month(data=data),
        "post_per_year": 1,
        "total_words": await total_words(data=data),
        "words_per_month": 7,
        "words_per_year": 7,
        "total_characters": await total_characters(data=data),
        "characters_per_month": 7,
        "characters_per_year": 7,
        "tag_count": 7,
        "mood_count": 7,
        "polarity_trend": 7,
        "subjectivity_trend": 7,
    
    }
    logger.debug(results)
    return results


async def posts_per_month(data: list):
    results: dict = {}
    for d in data:
        dt = d["date_created"]
        year_month = f"{dt.year}-{dt.month}"

        if year_month not in results:
            results[year_month] = 1
        else:
            results[year_month] += 1
    return results


async def posts_per_year(data: list):
    results: list = []
    for d in data:
        dt = d["date_created"]
        year = f"{dt.year}"

        for r in results:
            if r[year]:
                new = r[year] = r[year] + 1

                results.append(new)
        else:
            ym = {f"{year}": 1}
            results.append(ym)
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
    pass


async def words_per_month(data: list):
    pass


async def character_per_year(data: list):
    pass


async def words_per_year(data: list):
    pass


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
