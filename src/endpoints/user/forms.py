# -*- coding: utf-8 -*-
import logging
import re

from starlette_wtf import StarletteForm
from wtforms import PasswordField, TextField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.widgets import PasswordInput

from core.pass_lib import char_check, check_strength


class CreateAccountForm(StarletteForm):
    def check_pass(form, field):
        char = char_check(field.data)
        if char == False:
            raise ValidationError("An illegal character is present")

    def strong_pass(form, field):
        strength = check_strength(field.data)
        if strength == False:
            raise ValidationError("The password is too weak")

    def letter_number_only(form, field):
        logging.debug(f"validate that there are no illegal characters in {field.data}")
        data = re.match("^[A-Za-z0-9_-]*$", field.data)
        if data == None:
            raise ValidationError("Letters and numbers only")

    email = TextField(
        "Email address",
        validators=[
            DataRequired("Please enter your email address"),
            Email(),
        ],
    )
    user_name = TextField(
        "User Name",
        validators=[DataRequired("Please enter a user_name"), letter_number_only],
    )
    first_name = TextField(
        "First Name",
        validators=[
            DataRequired("Please enter your first name"),
        ],
    )
    last_name = TextField(
        "Last Name",
        validators=[
            DataRequired("Please enter your last name"),
        ],
    )
    password = PasswordField(
        "Password",
        widget=PasswordInput(hide_value=False),
        validators=[
            DataRequired("Please enter your password"),
            EqualTo("password_confirm", message="Passwords must match"),
            check_pass,
            strong_pass,
        ],
    )

    password_confirm = PasswordField(
        "Confirm Password",
        widget=PasswordInput(hide_value=False),
        validators=[DataRequired("Please confirm your password")],
    )


class AccountLoginForm(StarletteForm):
    user_name = TextField(
        "User Name",
        validators=[
            DataRequired("Please enter a user_name"),
        ],
    )
    password = PasswordField(
        "Password",
        widget=PasswordInput(hide_value=False),
        validators=[
            DataRequired("Please enter your password"),
        ],
    )


class UpdatePasswordForm(StarletteForm):
    def check_pass(form, field):
        char = char_check(field.data)
        if char == False:
            raise ValidationError("An illegal character is present")

    def strong_pass(form, field):
        strength = check_strength(field.data)
        if strength == False:
            raise ValidationError("The password is too weak")

    password = PasswordField(
        "Password",
        widget=PasswordInput(hide_value=False),
        validators=[
            DataRequired("Please enter your password"),
            EqualTo("password_confirm", message="Passwords must match"),
            check_pass,
            strong_pass,
        ],
    )

    password_confirm = PasswordField(
        "Confirm Password",
        widget=PasswordInput(hide_value=False),
        validators=[DataRequired("Please confirm your password")],
    )
