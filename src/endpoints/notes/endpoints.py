# -*- coding: utf-8 -*-

from loguru import logger
from starlette.responses import RedirectResponse

from core import login_required
from endpoints.notes import forms
from endpoints.notes.functions import (
    add_new_note,
    get_users_notes,
    get_note_id,
    get_users_tags,
)
from endpoints.user import crud as user_crud
from resources import templates
import silly

page_url = "/notes"


@login_required.require_login
async def notes_index(request):
    """
    Index page for notes
    """
    user_name = request.session["user_name"]
    user_data = await user_crud.user_info(user_name=user_name)
    user_data: dict = dict(user_data)
    user_data.pop("password")

    notes_result = await get_users_notes(user_name=user_name)

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

    form.note.data = """Veggies es bonus vobis, proinde vos postulo essum magis kohlrabi welsh onion daikon amaranth tatsoi tomatillo melon azuki bean garlic.

Gumbo beet greens corn soko endive gumbo gourd. Parsley shallot courgette tatsoi pea sprouts fava bean collard greens dandelion okra wakame tomato. Dandelion cucumber earthnut pea peanut soko zucchini.

Turnip greens yarrow ricebean rutabaga endive cauliflower sea lettuce kohlrabi amaranth water spinach avocado daikon napa cabbage asparagus winter purslane kale. Celery potato scallion desert raisin horseradish spinach carrot soko. Lotus root water spinach fennel kombu maize bamboo shoot green bean swiss chard seakale pumpkin onion chickpea gram corn pea. Brussels sprout coriander water chestnut gourd swiss chard wakame kohlrabi beetroot carrot watercress. Corn amaranth salsify bunya nuts nori azuki bean chickweed potato bell pepper artichoke.
    """
    # print(form.note.data)
    form.mood.data = "happy"
    some_tags = await get_users_tags(user_name=user_name)

    if await form.validate_on_submit():
        logger.debug(dict(form_data))

        tags_list: list = []
        for k, v in form_data.items():
            if k.startswith("tags-"):
                new_key = k.replace("tags-", "")
                tag_dict: dict = {new_key: v}
                tags_list.append(tag_dict)

        if len(tags_list) == 0:
            tags_list.append({"Unknown": True})

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


@login_required.require_login
async def notes_id(request):
    """
    Index page for notes
    """
    note_id = request.path_params["note_id"]
    user_name = request.session["user_name"]
    user_data = await user_crud.user_info(user_name=user_name)
    user_data: dict = dict(user_data)
    user_data.pop("password")
    note_result = await get_note_id(user_name=user_name, note_id=note_id)
    template = f"{page_url}/note_id.html"
    context = {
        "request": request,
        "user_data": user_data,
        "note": note_result,
    }
    logger.info(f"page accessed: /notes/{note_id}")
    return templates.TemplateResponse(template, context)
