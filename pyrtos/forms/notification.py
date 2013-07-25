from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    TextField,
    HiddenField,
    PasswordField,
    BooleanField,
)


class NotificationCreateForm(BaseForm):
    """
    Class constants representing form fields.

    """


class NotificationEditForm(NotificationCreateForm):
    """
    Class constants representing form fields.

    id -- category id, used in edit forms.
    """
    id = HiddenField()
