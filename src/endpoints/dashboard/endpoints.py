# -*- coding: utf-8 -*-

from loguru import logger

from core import login_required
from resources import templates

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
