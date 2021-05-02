# -*- coding: utf-8 -*-

from starlette_wtf import StarletteForm
from wtforms import BooleanField


class ApprovalReviewForm(StarletteForm):
    """Approve or Reject User"""

    is_active = BooleanField()
    is_admin = BooleanField(
        "Admin",
    )


# http://127.0.0.1:5000/htmx/user_search
