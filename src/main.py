# -*- coding: utf-8 -*-

import logging

from loguru import logger
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Mount
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from starlette_prometheus import PrometheusMiddleware
from starlette_prometheus import metrics
from starlette_wtf import CSRFProtectMiddleware

import resources
import settings
from app_functions import exceptions
from com_lib.logging_config import config_log
from app_functions.logger_middleware import LoggerMiddleware
from endpoints.admin import endpoints as admin_pages
from endpoints.dashboard import endpoints as dash_pages
from endpoints.notes import endpoints as note_pages
from endpoints.bots import endpoints as bot_pages
from endpoints.health import endpoints as health_pages
from endpoints.main import endpoints as main_pages
from endpoints.user import endpoints as user_pages
from resources import init_app


routes = [
    Route("/", main_pages.homepage, name="dashboard", methods=["GET", "POST"]),
    Route("/about", main_pages.about_page, methods=["GET"]),
    Mount(
        "/admin",
        routes=[
            Route("/open", endpoint=admin_pages.admin_index, methods=["GET", "POST"]),
            Route(
                "/all", endpoint=admin_pages.admin_all_requests, methods=["GET", "POST"]
            ),
            Route(
                "/review/{page}",
                endpoint=admin_pages.admin_review,
                methods=["GET", "POST"],
            ),
        ],
        name="user",
    ),
    Mount(
        "/dashboard",
        routes=[
            Route("/", endpoint=dash_pages.dashboard, methods=["GET"]),
        ],
        name="dashboard",
    ),
    Mount(
        "/notes",
        routes=[
            Route("/", endpoint=note_pages.notes_index, methods=["GET"]),
        ],
        name="notes",
    ),
    Mount(
        "/user",
        routes=[
            Route(
                "/forgot", endpoint=user_pages.forgot_password, methods=["GET", "POST"]
            ),
            Route("/login", endpoint=user_pages.login, methods=["GET", "POST"]),
            Route("/logout", endpoint=user_pages.logout, methods=["GET", "POST"]),
            Route(
                "/password-change",
                endpoint=user_pages.password_change,
                methods=["GET", "POST"],
            ),
            Route("/profile", endpoint=user_pages.profile, methods=["GET"]),
            Route("/register", endpoint=user_pages.register, methods=["GET", "POST"]),
        ],
        name="user",
    ),
    Route("/health", endpoint=health_pages.health_status, methods=["GET"]),
    Mount("/static", app=StaticFiles(directory="statics"), name="static"),
]


middleware = [
    Middleware(SessionMiddleware, secret_key=settings.SECRET_KEY),
    Middleware(CSRFProtectMiddleware, csrf_secret=settings.CSRF_SECRET),
    # Middleware(PrometheusMiddleware),
    Middleware(LoggerMiddleware),
]

exception_handlers = {
    403: exceptions.not_allowed,
    404: exceptions.not_found,
    500: exceptions.server_error,
}

init_app()
app = Starlette(
    debug=settings.DEBUG,
    routes=routes,
    middleware=middleware,
    exception_handlers=exception_handlers,
    on_startup=[resources.startup],
    on_shutdown=[resources.shutdown],
)
app.add_route("/metrics/", metrics)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info", debug=settings.DEBUG)
