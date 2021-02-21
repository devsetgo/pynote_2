# -*- coding: utf-8 -*-

import httpx
from loguru import logger
from starlette.responses import RedirectResponse

from core import login_required
from endpoints.configuration import forms
from endpoints.configuration.functions import add_new_tag, get_user_tags
from resources import templates

client = httpx.AsyncClient()


section = "configuration"
page_url = f"/{section}"


@login_required.require_login
async def index(request):
    """
    Index page for configuration
    """

    user_id = request.session["id"]
    # user_data = await user_crud.user_info(user_id=user_name)
    # user_data: dict = dict(user_data)
    # user_data.pop("password")

    tags_result = await get_user_tags(user_id=user_id)

    template = f"{page_url}/index.html"
    context = {
        "request": request,
        # "user_data": user_data,
        "tags": tags_result,
        "active": "config-index",
        "section": section,
    }
    logger.info(f"page accessed: /{section}")
    return templates.TemplateResponse(template, context)


@login_required.require_login
async def tag_view(request):
    """
    view tag
    """

    form = await forms.EditTag.from_formdata(request)
    form_data = await request.form()

    if await form.validate_on_submit():
        logger.debug(dict(form_data))
        return RedirectResponse(url="/configuration", status_code=303)
    template = f"{page_url}/tag-edit.html"
    context = {
        "request": request,
        "form": form,
        "active": "tag-view",
        "section": section,
    }
    logger.info(f"page accessed: /{section}/tag-edit")
    return templates.TemplateResponse(template, context)


@login_required.require_login
async def tag_new(request):
    """
    new tag
    """

    user_id = request.session["id"]

    form = await forms.NewTag.from_formdata(request)
    form_data = await request.form()

    if await form.validate_on_submit():

        logger.debug(dict(form_data))
        result = await add_new_tag(form_data=dict(form_data), user_id=user_id)
        logger.debug(result)
        if result == "is duplicate":
            form.name.errors.append(f"Duplicate tags not allowed")
            logger.info(
                f"form name {form_data['name']} is a duplicate for userid {user_id}"
            )
        else:
            return RedirectResponse(url="/configuration", status_code=303)

    template = f"{page_url}/tag-new.html"
    context = {
        "request": request,
        "form": form,
        "active": "tag-new",
        "section": section,
    }
    logger.info(f"page accessed: /{section}/new")
    return templates.TemplateResponse(template, context)


@login_required.require_login
async def tag_edit(request):
    """
    edit tag
    """
    user_name = request.session["user_name"]

    logger.debug(f"request")
    form = await forms.NewNote.from_formdata(request)
    form_data = await request.form()
    form.note.data = "this is my textarea content!"
    form.mood.data = "sad"
    if await form.validate_on_submit():
        logger.critical(dict(form_data))
        logger.warning(form_data["tags"])
    template = f"{page_url}/tag-edit.html"
    context = {
        "request": request,
        "form": form,
        "active": "tag-edit",
        "section": section,
    }
    logger.info(f"page accessed: /{section}/tag-edit")
    return templates.TemplateResponse(template, context)
