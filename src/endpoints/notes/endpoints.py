# -*- coding: utf-8 -*-
import logging

from loguru import logger
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from endpoints.user import crud as user_crud
from resources import templates
from app_functions.db_setup import users

from app_functions import login_required

page_url = "/notes_pages"

@login_required.require_login
async def notes_index(request):
    """
    Index page for notes
    """
    user_name=request.session['user_name']
    user_data = await user_crud.user_info(user_name=user_name)
    user_data:dict = dict(user_data)
    template = f"{page_url}/index.html"
    context = {
        "request": request,
        "user_data": user_data,
    }
    logger.info("page accessed: /notes")
    return templates.TemplateResponse(template, context)