# -*- coding: utf-8 -*-

from loguru import logger
from starlette.responses import RedirectResponse

from core import login_required
from endpoints.notes import forms
from endpoints.notes.functions import (
    add_new_note,
    get_note_id,
    get_users_notes,
    get_users_tags,
)
from endpoints.user import crud as user_crud
from resources import templates

section = "notes"
page_url = f"/{section}"


@login_required.require_login
async def notes_index(request):
    """
    Index page for notes
    """
    user_id = request.session["id"]
    user_name = request.session["user_name"]
    user_data = await user_crud.user_info(user_name=user_name)
    user_data: dict = dict(user_data)
    user_data.pop("password")

    notes_result = await get_users_notes(user_id=user_id)
    form = await forms.Direction.from_formdata(request)

    template = f"{page_url}/index.html"
    context = {
        "request": request,
        "user_data": user_data,
        "notes": notes_result,
        "active": "note-index",
        "section": section,
        "form": form,
    }
    logger.info("page accessed: /notes")
    return templates.TemplateResponse(template, context)


@login_required.require_login
async def notes_direction(request):
    """
    Index page for notes
    """
    user_id = request.session["id"]
    user_name = request.session["user_name"]
    form = await forms.Direction.from_formdata(request)

    form_data = await request.form()

    logger.debug(form_data)
    user_data = await user_crud.user_info(user_name=user_name)
    user_data: dict = dict(user_data)
    user_data.pop("password")

    limit_value: int = int(form_data["limit"])
    off_set_value: int = 0
    if "btn-previous" in form_data:
        off_set_value: int = int(form_data["off_set"]) - limit_value

    elif "btn-next" in form_data:
        off_set_value: int = int(form_data["off_set"]) + limit_value

    if off_set_value < 0:
        off_set_value: int = 0
        logger.info(f"Offset value is less than zero, setting to 0 offset")

    logger.info(f"offset set to {off_set_value}")

    notes_result = await get_users_notes(
        user_id=user_id, off_set=off_set_value, limit=limit_value
    )

    template = f"{page_url}/index.html"
    context = {
        "request": request,
        "user_data": user_data,
        "notes": notes_result,
        "active": "note-index",
        "section": section,
        "form": form,
    }
    logger.info("page accessed: /notes")
    return templates.TemplateResponse(template, context)


@login_required.require_login
async def notes_new(request):
    """
    new note
    """
    user_name = request.session["user_name"]
    user_id = request.session["id"]

    form = await forms.NewNote.from_formdata(request)

    form_data = await request.form()

    from endpoints.notes import pg

    para = [
        pg.p_1,
        pg.p_2,
        pg.p_3,
    ]

    # form.note.data = para[random.randint(0, 2)]
    # print(form.note.data)
    tags = await get_users_tags(user_id=user_id)

    if await form.validate_on_submit():
        logger.debug(dict(form_data))

        tags_list: list = []
        for k, v in form_data.items():

            if k.startswith("tags-"):
                new_key = k.replace("tags-", "")
                tag_dict: dict = {new_key: v}
                logger.debug(tag_dict)
                tags_list.append(tag_dict)

        if len(tags_list) == 0:
            tags_list.append({"Unknown": True})

        # tags_dict: dict = {"tags": tags_list}
        data: dict = {"form_data": form_data, "tags": tags_list}
        logger.debug(data)
        result = await add_new_note(data=data, user_name=user_name)
        logger.debug(result)
        if result is not None:
            d = await form.validate()

        if "btn-another" in form_data:
            return RedirectResponse(url="/notes/new", status_code=303)
        else:
            return RedirectResponse(url="/notes", status_code=303)

    template = f"{page_url}/new.html"
    context = {
        "request": request,
        "form": form,
        "all_tags": tags,
        "active": "note-new",
        "section": section,
    }
    logger.info("page accessed: /notes/new")
    return templates.TemplateResponse(template, context)


@login_required.require_login
async def notes_id(request):
    """
    Index page for notes
    """

    note_id = request.path_params["note_id"]
    user_name = request.session["user_name"]
    user_id = request.session["id"]
    user_data = await user_crud.user_info(user_name=user_name)
    user_data: dict = dict(user_data)
    user_data.pop("password")
    note_result = await get_note_id(user_id=user_id, note_id=note_id)
    template = f"{page_url}/note_id.html"
    context = {
        "request": request,
        "user_data": user_data,
        "note": note_result,
        "active": "note-id",
        "section": section,
    }
    logger.info(f"page accessed: /notes/{note_id}")
    return templates.TemplateResponse(template, context)
