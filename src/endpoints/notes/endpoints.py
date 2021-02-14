# -*- coding: utf-8 -*-
import logging

from loguru import logger
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from app_functions import login_required
from app_functions.db_setup import users
from endpoints.notes.functions import users_notes, add_new_note
from endpoints.user import crud as user_crud
from resources import templates
from endpoints.notes import forms

page_url = "/notes_pages"


@login_required.require_login
async def notes_index(request):
    """
    Index page for notes
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
    logger.info("page accessed: /notes")
    return templates.TemplateResponse(template, context)


@login_required.require_login
async def notes_new(request):
    """
    new note
    """
    user_name = request.session["user_name"]

    logger.debug(f"request")
    form = await forms.NewNote.from_formdata(request)
    form_data = await request.form()
    form.note.data = "this is my textarea content!"
    form.mood.data = "sad"
    # ToDo: make query to get Tags by user and standard
    some_tags = ["dev", "life", "code", "this", "that", "another", "and another"]
    if await form.validate_on_submit():
        logger.debug(dict(form_data))

        tags_list: list = []
        for k, v in form_data.items():
            if k.startswith("tags-"):
                new_key = k.replace("tags-", "")
                tag_dict: dict = {new_key: v}
                tags_list.append(tag_dict)

        # tags_dict: dict = {"tags": tags_list}
        data: dict = {"form_data": form_data, "tags": tags_list}
        logger.critical(data)
        result = await add_new_note(data=data, user_name=user_name)
        logger.critical(result)
        return RedirectResponse(url="/notes", status_code=303)

    template = f"{page_url}/new.html"
    context = {
        "request": request,
        "form": form,
        "some_tags": some_tags,
    }
    logger.info("page accessed: /notes/new")
    return templates.TemplateResponse(template, context)
