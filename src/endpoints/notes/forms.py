# -*- coding: utf-8 -*-
import logging
import re

from loguru import logger
from starlette_wtf import StarletteForm
import wtforms

# import SelectField, SelectMultipleField, TextAreaField, TextField
from wtforms import validators

#  import DataRequired, EqualTo, Length, ValidationError

# from com_lib.pass_lib import char_check
# from com_lib.pass_lib import check_strength


class NewNote(StarletteForm):

    note = wtforms.TextAreaField(
        "Requirements",
        render_kw={"rows": 10, "cols": 80},
        validators=[
            validators.DataRequired("Your note"),
            validators.Length(min=1, max=5000),
        ],
    )
    mood = wtforms.SelectField(
        "Choose an option",
        choices=["-", "happy", "sad", "left of center"],
        validate_choice=False,
    )
    tags = wtforms.SelectMultipleField(
        "Choose one or more",
        choices=[("1", "C++"), ("2", "Python"), ("3", "JAVA")],
        default=["1", "3"],
    )


# choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')]
# class CreateAccountForm(StarletteForm):
#     def check_pass(form, field):
#         char = char_check(field.data)
#         if char == False:
#             raise ValidationError("An illegal character is present")

#     def strong_pass(form, field):
#         strength = check_strength(field.data)
#         if strength == False:
#             raise ValidationError("The password is too weak")

#     def letter_number_only(form, field):
#         logging.debug(f"validate that there are no illegal characters in {field.data}")
#         data = re.match("^[A-Za-z0-9_-]*$", field.data)
#         if data == None:
#             raise ValidationError("Letters and numbers only")

#     email = TextField(
#         "Email address",
#         validators=[
#             DataRequired("Please enter your email address"),
#             Email(),
#         ],
#     )
#     user_name = TextField(
#         "User Name",
#         validators=[DataRequired("Please enter a user_name"), letter_number_only],
#     )
#     first_name = TextField(
#         "First Name",
#         validators=[
#             DataRequired("Please enter your first name"),
#         ],
#     )
#     last_name = TextField(
#         "Last Name",
#         validators=[
#             DataRequired("Please enter your last name"),
#         ],
#     )
#     password = PasswordField(
#         "Password",
#         widget=PasswordInput(hide_value=False),
#         validators=[
#             DataRequired("Please enter your password"),
#             EqualTo("password_confirm", message="Passwords must match"),
#             check_pass,
#             strong_pass,
#         ],
#     )

#     password_confirm = PasswordField(
#         "Confirm Password",
#         widget=PasswordInput(hide_value=False),
#         validators=[DataRequired("Please confirm your password")],
#     )


# class AccountLoginForm(StarletteForm):
#     user_name = TextField(
#         "User Name",
#         validators=[
#             DataRequired("Please enter a user_name"),
#         ],
#     )
#     password = PasswordField(
#         "Password",
#         widget=PasswordInput(hide_value=False),
#         validators=[
#             DataRequired("Please enter your password"),
#         ],
#     )


# class UpdatePasswordForm(StarletteForm):
#     def check_pass(form, field):
#         char = char_check(field.data)
#         if char == False:
#             raise ValidationError("An illegal character is present")

#     def strong_pass(form, field):
#         strength = check_strength(field.data)
#         if strength == False:
#             raise ValidationError("The password is too weak")

#     password = PasswordField(
#         "Password",
#         widget=PasswordInput(hide_value=False),
#         validators=[
#             DataRequired("Please enter your password"),
#             EqualTo("password_confirm", message="Passwords must match"),
#             check_pass,
#             strong_pass,
#         ],
#     )

#     password_confirm = PasswordField(
#         "Confirm Password",
#         widget=PasswordInput(hide_value=False),
#         validators=[DataRequired("Please confirm your password")],
#     )
