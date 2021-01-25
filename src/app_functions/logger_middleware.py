import logging

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        
        method = request.method
        url = request.url
        client = request.client.host
        print(type(url),type(client))
        logger.info(f"{method.capitalize()} request via {url} accessed from {client}")
        # response.headers['Custom'] = 'Example'
        return response
