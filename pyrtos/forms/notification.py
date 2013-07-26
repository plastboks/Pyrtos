from pyrtos.forms.meta import BaseForm, strip_filter

from pyrtos.models import Notification

from wtforms import (
    validators,
    widgets,
    TextField,
    HiddenField,
    PasswordField,
    BooleanField,
    SelectField,
    SelectMultipleField,
)


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class NotificationCreateForm(BaseForm):
    """
    Class constants representing form fields.

    title -- string, title
    hour -- selector, hour
    minutes -- selector, minute
    """
    title = TextField('Title',
                      [validators.Length(min=1, max=255)],
                      filters=[strip_filter])
    weekfilter = MultiCheckboxField('Days',
                                    coerce=unicode,
                                    choices=Notification.days,
                                    )
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
