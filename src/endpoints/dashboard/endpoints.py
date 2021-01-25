# -*- coding: utf-8 -*-
import logging

from loguru import logger
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from endpoints.bots import crud as bot_crud
from resources import templates

from app_functions import login_required

page_url = "/dashboard_pages"

@login_required.require_login
async def dashboard(request):
    """
    Index page for twitter bots
    """

    template = f"{page_url}/index.html"
    context = {
        "request": request,
        # "bots": bots_list,
    }
    logger.info("page accessed: /dashboard")
    return templates.TemplateResponse(template, context)

async def about_page(request):

    template = f"about.html"
    context = {"request": request}
    logger.info(f"page accessed: /{template}")
    return templates.TemplateResponse(template, context)



