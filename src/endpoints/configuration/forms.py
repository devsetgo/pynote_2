# -*- coding: utf-8 -*-

import wtforms
from starlette_wtf import StarletteForm
from wtforms import validators


class NewTag(StarletteForm):

    name = wtforms.TextField(
        "name",
        validators=[
            validators.DataRequired("Tag name"),
        ],
    )
    is_active = wtforms.BooleanField(
        "active state", default=True, render_kw={"checked": ""}
    )
    default_value = wtforms.BooleanField("default value", default=False)


class EditTag(StarletteForm):

    name = wtforms.TextField(
        "name",
        validators=[
            validators.DataRequired("Tag name"),
        ],
    )
    # is_active = wtforms.BooleanField(
    #     "active state", default=True, render_kw={"checked": ""}
    # )
    # default_value = wtforms.BooleanField("default value", default=False)
