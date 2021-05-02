# -*- coding: utf-8 -*-

import wtforms
from starlette_wtf import StarletteForm
from wtforms import validators

MOODS: list = ["Positive", "Neutral", "Negative"]


class Direction(StarletteForm):
    limit = wtforms.SelectField(
        "limit",
        choices=[
            ("20", 20),
            ("50", 50),
            ("100", 100),
        ],
    )
    off_set = wtforms.HiddenField()


class NewNote(StarletteForm):

    note = wtforms.TextAreaField(
        "Note",
        render_kw={"rows": 10, "cols": 80},
        validators=[
            validators.DataRequired("Enter your note!"),
            validators.Length(min=10, max=5000),
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
