from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    widgets,
    TextField,
    FloatField,
    DateField,
    DateTimeField,
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
    from_date = DateTimeField('From date', format='%Y-%m-%d %H:%M')
    to_date = DateTimeField('To date', format='%Y-%m-%d %H:%M')
    private = BooleanField('Private')
    reminder_true = BooleanField('Reminder')
    reminder_alert = DateTimeField('Alert time',
                               [validators.Optional()],
                               format='%Y-%m-%d %H:%M',
                               )


class EventEditForm(EventCreateForm):
    """
    Class constants representing form fields.

    id -- event id, used in edit forms.
    """
    id = HiddenField()
