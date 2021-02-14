# -*- coding: utf-8 -*-
import datetime
import uuid

from loguru import logger
from starlette.responses import RedirectResponse
from starlette_wtf import csrf_protect

from core import login_required
from core.crud_ops import execute_one_db, fetch_one_db
from core.db_setup import user_login_failures, users
from core.pass_lib import encrypt_pass
from endpoints.admin.crud import create_review_user
from endpoints.user import crud as user_crud
from endpoints.user import form_validators, forms
from resources import templates

page_url = "/user"


@csrf_protect
async def login(request):
    logger.debug(f"request")
    form = await forms.AccountLoginForm.from_formdata(request)
    form_data = await request.form()

    if await form.validate_on_submit():
        logger.debug(form_data)
        user_name = form_data["user_name"]
        user_name = user_name.lower()
        pwd = form_data["password"]
        logger.debug(f"user_name: {user_name}, pwd: {pwd}")

        result = await form_validators.valid_login(pwd=pwd, user_name=user_name)
        logger.debug(f"loging valid = {result}")

        # user_name = user_name.lower()
        logger.debug(f"checking if {user_name.lower()} has valid login")
        query = users.select().where(users.c.user_name == user_name)
        logger.info(f"fetch user_name: {user_name}")
        user_data = await fetch_one_db(query)
        logger.debug(f"LOOK AT THIS query result = {user_data}")

        last_login_values = {"last_login": datetime.datetime.now()}
        last_login_query = users.update().where(users.c.user_name == user_name)
        await execute_one_db(query=last_login_query, values=last_login_values)
        logger.info(f"updating last login for {user_name}")
        if result == False:
            client_host = request.client.host
            fail_values: dict = {
                "id": str(uuid.uuid4()),
                "date_created": datetime.datetime.now(),
                "user_name": user_name,
                "ip_address": client_host,
            }
            fail_query = user_login_failures.insert()
            await execute_one_db(query=fail_query, values=fail_values)
            logger.warning(f"User login failure for {user_name} from {client_host}")
            form.user_name.errors.append(f"user_name or Password is invalid")

        elif user_data["is_active"] == False:
            form.user_name.errors.append(
                f"The user id is not active or been approved for login"
            )
        else:
            # get user user_name

            request.session["user_name"] = user_data["user_name"]
            request.session["updated"] = str(datetime.datetime.now())
            request.session["admin"] = user_data["is_admin"]
            request.session[
                "realname"
            ] = f'{user_data["first_name"]} {user_data["last_name"]}'
            logger.info(
                f'logger {request.session["user_name"]} and send to profile page'
            )
            return RedirectResponse(url="/", status_code=303)

    template = f"{page_url}/login.html"
    context = {"request": request, "form": form}
    logger.info(f"page accessed: /user/login")
    return templates.TemplateResponse(template, context)


@csrf_protect
async def register(request):
    form = await forms.CreateAccountForm.from_formdata(request)
    form_data = await request.form()

    if await form.validate_on_submit():
        # check if unique email
        email_check = await form_validators.email_check(form_data["email"])

        # check if unique user_name
        user_name_check = await form_validators.user_name_check(form_data["user_name"])

        if email_check != None:
            if email_check["email"] == form_data["email"]:
                logger.error(f'{form_data["email"]} exists in database')
                form.email.errors.append(f"the email exists within database")

        elif user_name_check != None:
            if user_name_check["user_name"] == form_data["user_name"]:
                logger.error(f'{form_data["user_name"]} exists in database')
                form.user_name.errors.append(f"the user_name exists within database")

        else:
            hashed_pwd = encrypt_pass(form_data["password"])
            values = {
                "first_name": form_data["first_name"],
                "last_name": form_data["last_name"],
                "user_name": form_data["user_name"].lower(),
                "password": hashed_pwd,
                "email": form_data["email"].lower(),
            }
            logger.debug(values)
            await user_crud.user_register(data=values)
            await create_review_user(form_data["user_name"].lower())
            logger.info("Redirecting user to index page /")
            return RedirectResponse(url="/", status_code=303)

    status_code = 422 if form.errors else 200

    template = "/user/register.html"
    context = {"request": request, "form": form}
    logger.info(f"page accessed: /user/register")
    return templates.TemplateResponse(template, context, status_code=status_code)


@login_required.require_login
async def logout(request):
    logger.info(f'logout request {request.session["user_name"]}')
    request.session.clear()
    # url = request.url_for("dashboard")
    return RedirectResponse(url="/", status_code=303)


@csrf_protect
@login_required.require_login
async def password_change(request):

    form = await forms.UpdatePasswordForm.from_formdata(request)
    form_data = await request.form()

    if await form.validate_on_submit():
        # TODO: make this work
        hashed_pwd = encrypt_pass(form_data["password"])
        query = users.update().where(users.c.user_name == request.session["user_name"])
        values = {
            "password": hashed_pwd,
        }
        logger.debug(values)
        db_result = await execute_one_db(query=query, values=values)
        logger.info("Redirecting user to index page /")
        return RedirectResponse(url="/", status_code=303)

    status_code = 200
    template = f"{page_url}/password.html"
    context = {"request": request, "form": form}
    logger.info(f"page accessed: /user/password-change")
    return templates.TemplateResponse(template, context, status_code=status_code)


@login_required.require_login
async def forgot_password(request):
    status_code = 200
    template = f"{page_url}/forgot-password.html"
    context = {"request": request, "greeting": "hi"}
    return templates.TemplateResponse(template, context, status_code=status_code)


@login_required.require_login
async def profile(request):
    user_name = request.session["user_name"]

    user_data = await user_crud.user_info(user_name=user_name)
    user_data = dict(user_data)
    pop_list: list = ["password", "first_login", "from_config"]
    for p in pop_list:
        user_data.pop(p, None)
    status_code = 200
    template = f"{page_url}/profile.html"
    context = {"request": request, "user_data": user_data}
    return templates.TemplateResponse(template, context, status_code=status_code)
