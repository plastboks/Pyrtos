from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    widgets,
    TextField,
    FloatField,
    DateField,
    HiddenField,
    SelectField,
    PasswordField,
    SelectMultipleField,
    FileField,
    BooleanField,
)


class EventCreateForm(BaseForm):
    """
    Class constants representing form fields.

    title -- Event title.
    from_date = Datefield, from date.
    to_date = Datefield, to date.
    """
    title = TextField('Event title',
                      [validators.Length(min=2, max=255)],
                      filters=[strip_filter])
    from_date = DateField('From date', format='%Y-%m-%d')
    to_date = DateField('To date', format='%Y-%m-%d')
    private = BooleanField('Private')
    reminder = BooleanField('Reminder')
    reminder_alert = DateField('Alert time', format='%Y-%m-%d')


class EventEditForm(EventCreateForm):
    """
    Class constants representing form fields.

    id -- event id, used in edit forms.
    """
    id = HiddenField()
