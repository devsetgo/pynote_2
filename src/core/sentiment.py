# -*- coding: utf-8 -*-
"""
textblob functions
"""
from textblob import TextBlob


def sentiment_check(text_str: str):
    data = TextBlob(text_str)
    result = data.sentiment
    print(result)
    return result
