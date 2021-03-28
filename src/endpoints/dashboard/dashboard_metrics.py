# -*- coding: utf-8 -*-


from loguru import logger

from core.colors import HEX_COLORS, RGBa_COLORS
from core.crud_ops import fetch_all_db
from core.db_setup import notes


async def get_metrics(user_id: str):
    query = (
        notes.select()
        .where(notes.c.user_id == user_id)
        .order_by(notes.c.date_created.desc())
    )
    logger.debug(f"user posts query: {query}")
    data = await fetch_all_db(query)
    logger.debug(f"Query result = {data}")
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
    return results


async def posts_per_month(data: list):

    years: list = []
    for d in data:
        year = str(d["created_year"])
        if year not in years:
            years.append(year)
    results: list = []
    color_number: int = 0
    for y in years:

        year_month: list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for m in data:
            if str(m["created_year"]) == y:
                year_month[m["created_month"] - 1] += 1
        c = RGBa_COLORS[color_number]
        year_data: dict = {
            "year": y,
            "data": year_month,
            "backgroundColor": f"rgba({c[0]},{c[1]},{c[2]},0.9)",
            "borderColor": f"rgba({c[0]},{c[1]},{c[2]},0.8)",
            "pintStrokeColor": f"rgba({c[0]},{c[1]},{c[2]},1)",
            "pointHighlightStroke": f"rgba({c[0]},{c[1]},{c[2]},1)",
        }
        results.append(year_data)
        color_number += 1
    logger.debug(results)
    return results
    # return years


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
    logger.debug(results)
    return results


async def total_characters(data: list):
    counts: list = []
    for d in data:
        counts.append(d["char_count"])
    results: int = sum(counts)
    logger.debug(results)
    return results


async def total_words(data: list):
    counts: list = []
    for d in data:
        counts.append(d["word_count"])
    results: int = sum(counts)
    logger.debug(results)
    return results


async def character_per_month(data: list):

    years: list = []
    for d in data:
        year = str(d["created_year"])
        if year not in years:
            years.append(year)
    results: list = []
    color_number: int = 0
    for y in years:

        year_month: list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for m in data:
            if str(m["created_year"]) == y:
                year_month[m["created_month"] - 1] += m["char_count"]
        c = RGBa_COLORS[color_number]
        year_data: dict = {
            "year": y,
            "data": year_month,
            "backgroundColor": f"rgba({c[0]},{c[1]},{c[2]},0.9)",
            "borderColor": f"rgba({c[0]},{c[1]},{c[2]},0.8)",
            "pintStrokeColor": f"rgba({c[0]},{c[1]},{c[2]},1)",
            "pointHighlightStroke": f"rgba({c[0]},{c[1]},{c[2]},1)",
        }
        results.append(year_data)
        color_number += 1
    logger.debug(results)
    # print(results)
    return results


async def words_per_month(data: list):

    years: list = []
    for d in data:
        year = str(d["created_year"])
        if year not in years:
            years.append(year)
    results: list = []
    color_number: int = 0
    for y in years:

        year_month: list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for m in data:
            if str(m["created_year"]) == y:
                year_month[m["created_month"] - 1] += m["word_count"]
        c = RGBa_COLORS[color_number]
        year_data: dict = {
            "year": y,
            "data": year_month,
            "backgroundColor": f"rgba({c[0]},{c[1]},{c[2]},0.9)",
            "borderColor": f"rgba({c[0]},{c[1]},{c[2]},0.8)",
            "pintStrokeColor": f"rgba({c[0]},{c[1]},{c[2]},1)",
            "pointHighlightStroke": f"rgba({c[0]},{c[1]},{c[2]},1)",
        }
        results.append(year_data)
        color_number += 1
    logger.debug(results)
    # print(results)
    return results


async def character_per_year(data: list):
    data_dict: dict = {}

    for d in data:
        year = str(d["created_year"])

        if year not in data_dict:
            data_dict[year] = d["char_count"]
        else:
            data_dict[year] += d["char_count"]

    results: dict = {
        "years": list(data_dict.keys()),
        "data": list(data_dict.values()),
        "qty": len(list(data_dict.keys())),
    }
    logger.debug(results)
    return results


async def words_per_year(data: list):
    data_dict: dict = {}

    for d in data:
        year = str(d["created_year"])

        if year not in data_dict:
            data_dict[year] = d["word_count"]
        else:
            data_dict[year] += d["word_count"]

    results: dict = {
        "years": list(data_dict.keys()),
        "data": list(data_dict.values()),
        "qty": len(list(data_dict.keys())),
    }
    logger.debug(results)
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
