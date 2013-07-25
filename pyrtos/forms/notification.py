from pyrtos.forms.meta import BaseForm, strip_filter

from pyrtos.models import Notification

from wtforms import (
    validators,
    TextField,
    HiddenField,
    PasswordField,
    BooleanField,
    SelectField,
)


class NotificationCreateForm(BaseForm):
    """
    Class constants representing form fields.

    hour -- hour selector
    minutes -- minute selector
    """
    hour = SelectField('Hour',
                       choices=[(n, "%02d" % n)
                                for n in Notification.hour])
    minute = SelectField('Minute',
                         choices=[(n, "%02d" % n)
                                  for n in Notification.minute])


class NotificationEditForm(NotificationCreateForm):
    """
    Class constants representing form fields.

    id -- category id, used in edit forms.
    """
    id = HiddenField()
