# -*- coding: utf-8 -*-
import logging
from os import stat_result

from loguru import logger
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from app_functions import login_required
from app_functions.db_setup import users
from endpoints.notes.functions import users_notes
from endpoints.user import crud as user_crud
from resources import templates
from endpoints.notes import forms


section="htmx"
page_url = f"/{section}_pages"

@login_required.require_login
async def htmx_index(request):
    """
    Index page for htmx
    """
    user_name = request.session["user_name"]
    user_data = await user_crud.user_info(user_name=user_name)
    user_data: dict = dict(user_data)
    user_data.pop("password")

    notes_result = await users_notes(user_name=user_name)

    template = f"{page_url}/index.html"
    context = {
        "request": request,
        "user_data": user_data,
        "notes": notes_result,
    }
    logger.info(f"page accessed: /{section}")
    return templates.TemplateResponse(template, context)


@login_required.require_login
async def htmx_new(request):
    """
    new htmx
    """
    user_name = request.session["user_name"]

    logger.debug(f"request")
    form = await forms.NewNote.from_formdata(request)
    form_data = await request.form()
    form.note.data='this is my textarea content!'
    form.mood.data='sad'
    if await form.validate_on_submit():
        logger.critical(dict(form_data))
        logger.warning(form_data['tags'])
    template = f"{page_url}/new.html"
    context = {
        "request": request,
        "form": form,
    }
    logger.info(f"page accessed: /{section}/new")
    return templates.TemplateResponse(template, context)

import httpx
client = httpx.AsyncClient()


async def filler(request):
    form_data = await request.form()
    para = form_data["search"]
    logger.critical(para)
    url=f'https://test-api.devsetgo.com/api/v1/groups/list?groupName={para}'
    r = await client.get(url)

    resp = r.json()
    user_data = resp['groups']

    context = {
        "request": request,
        "user_data": user_data,
    }
    template = f"{page_url}/user_data.html"
    logger.info(f"page accessed: /{section}/search")
    return templates.TemplateResponse(template, context)
