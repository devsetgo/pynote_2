# -*- coding: utf-8 -*-

from loguru import logger
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from datetime import datetime
from core import login_required
from resources import templates
from loguru import logger
from sqlalchemy import and_
import time
from core.crud_ops import execute_one_db, fetch_all_db, fetch_one_db
from core.db_setup import notes, tags


@login_required.require_login
async def index(request):

    template = f"htmx/index.html"
    context = {"request": request}
    logger.info(f"page accessed: /htmx/{template}")
    return templates.TemplateResponse(template, context)


@login_required.require_login
async def user_search(request):

    # data = await search_notes(
    #     user_id=request.session["id"], terms=request.query_params["search"]
    # )
    user_id=request.session["id"]
    terms=request.query_params["search"]
    query = (
        notes.select()
        .where(notes.c.user_id == user_id)
        .where(notes.c.note.ilike(f"%{terms}%"))
        .limit(100)
        .order_by(notes.c.date_created.desc())
    )

    try:
        # query database
        results = await fetch_all_db(query=query)
    except Exception as e:
        logger.error(f"error: {e}")
        results = []

    template = f"htmx/note_data.html"
    context = {"request": request, "data": results}
    logger.info(f"page accessed: /htmx/{template}")
    return templates.TemplateResponse(template, context)


# get notes for user
async def search_notes(user_id: str, terms: str = None):
    
    query = (
        notes.select()
        .where(notes.c.user_id == user_id)
        .where(notes.c.note.ilike(f"%{terms}%"))
        .limit(100)
        .order_by(notes.c.date_created.desc())
    )

    try:
        # query database
        results = await fetch_all_db(query=query)
        return results
    except Exception as e:
        logger.error(f"error: {e}")
