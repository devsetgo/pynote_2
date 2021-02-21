# -*- coding: utf-8 -*-

import wtforms
from starlette_wtf import StarletteForm
from wtforms import validators

MOODS: list = ["positive", "neutral", "negative"]


class NewNote(StarletteForm):

    note = wtforms.TextAreaField(
        "Note",
        render_kw={"rows": 10, "cols": 80},
        validators=[
            validators.DataRequired("Enter your note!"),
            validators.Length(min=1, max=5000),
        ],
    )
    mood = wtforms.RadioField(
        "Choose your moode",
        choices=MOODS,
        validate_choice=False,
        validators=[validators.DataRequired()],
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
    mood = wtforms.RadioField(
        "Choose your moode",
        choices=MOODS,
        validate_choice=False,
        validators=[validators.DataRequired()],
    )
