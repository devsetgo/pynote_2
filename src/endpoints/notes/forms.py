# -*- coding: utf-8 -*-

import wtforms
from starlette_wtf import StarletteForm
from loguru import logger
from wtforms import validators


moods:list=["-", "positive", "neutral", "negative"]


class NewNote(StarletteForm):

    def no_dash(form, field):
        logger.debug(f"validate that '-' is not in {field.data}")
        # data = re.match("^[A-Za-z0-9_-]*$", field.data)
        if field.data == "-":
            raise wtforms.validators.ValidationError("Letters and numbers only")

    note = wtforms.TextAreaField(
        "Note",
        render_kw={"rows": 10, "cols": 80},
        validators=[
            validators.DataRequired("Enter your note!"),
            validators.Length(min=1, max=5000),
        ],
    )
    mood = wtforms.SelectField(
        "Choose an option",
        choices=moods,
        validate_choice=False,
        validators=[no_dash]
    )


class EditNote(StarletteForm):
    
    def no_dash(form, field):
        logger.debug(f"validate that '-' is not in {field.data}")
        # data = re.match("^[A-Za-z0-9_-]*$", field.data)
        if field.data == "-":
            raise wtforms.validators.ValidationError("Letters and numbers only")
    
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
        choices=moods,
        validate_choice=False,
        validators=[no_dash]
    )
