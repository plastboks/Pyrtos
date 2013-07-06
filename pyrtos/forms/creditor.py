from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    TextField,
    HiddenField,
    PasswordField,
)

class CreditorCreateForm(BaseForm):
    title = TextField('Creditor Title',
                      [validators.Length(max=255)],
                      filters=[strip_filter])

class CreditorEditForm(CreditorCreateForm):
    id = HiddenField()
