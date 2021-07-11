# -*- coding: utf-8 -*-

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all requests made to application
    """

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        method = request.method
        url = request.url
        client = request.client.host
       
        if "id" in request.session:
            user_id = request.session["id"]
        else:
           user_id = "unknown guest" 
        

        if "favicon.ico" not in str(url):
            logger.info(
                f"Request Method: {method.upper()} request via {url} accessed from {client} by {user_id}"
            )
            logger.debug(f"full_request_data: {dict(request)}")
        return response
