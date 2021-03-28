# -*- coding: utf-8 -*-

from loguru import logger

from core import login_required
from endpoints.dashboard.dashboard_metrics import get_metrics
from resources import templates

page_url = "/dashboard"


@login_required.require_login
async def dashboard(request):
    """
    Dashboard
    """
    user_id = request.session["id"]
    dashboard_metrics = await get_metrics(user_id=user_id)
    # print(dashboard_metrics)
    template = f"{page_url}/index.html"
    context = {
        "request": request,
        "metrics": dashboard_metrics,
    }
    logger.info("page accessed: /dashboard")
    return templates.TemplateResponse(template, context)


async def about_page(request):

    template = f"about.html"
    context = {"request": request}
    logger.info(f"page accessed: /{template}")
    return templates.TemplateResponse(template, context)
