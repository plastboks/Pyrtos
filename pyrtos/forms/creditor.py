from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    TextField,
    HiddenField,
    PasswordField,
    BooleanField,
)


class CreditorCreateForm(BaseForm):
    title = TextField('Creditor Title',
                      [validators.Length(min=3, max=255)],
                      filters=[strip_filter])
    private = BooleanField('Private', default=False)


class CreditorEditForm(CreditorCreateForm):
    id = HiddenField()
