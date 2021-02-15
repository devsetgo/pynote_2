# -*- coding: utf-8 -*-

import wtforms
from starlette_wtf import StarletteForm

from wtforms import validators


class NewNote(StarletteForm):

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
        choices=["-", "happy", "sad", "left of center"],
        validate_choice=False,
    )


class EditNote(StarletteForm):
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
