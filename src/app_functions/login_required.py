# -*- coding: utf-8 -*-
import logging
from typing import Callable
from datetime import datetime,timedelta
from loguru import logger
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.responses import Response
import settings


def require_login(endpoint: Callable) -> Callable:
    async def check_login(request: Request) -> Response:

        
        if "user_name" not in request.session:
            logger.error(
                f"user page access without being logged in from {request.client.host}"
            )
            return RedirectResponse(url="/user/login", status_code=303)

        else:
            one_twenty = datetime.utcnow() - timedelta(minutes = settings.LOGIN_TIMEOUT)
            current:bool = one_twenty < datetime.strptime(request.session["updated"], '%Y-%m-%d %H:%M:%S.%f')
            
            if current==False:
                logger.error(f"user {request.session['user_name']} outside window: {current}")
                return RedirectResponse(url="/user/login", status_code=303)

            # update datetime of last use
            logger.info(f"user {request.session['user_name']} within window: {current}")
            request.session["updated"] = str(datetime.utcnow())
        return await endpoint(request)

    return check_login
