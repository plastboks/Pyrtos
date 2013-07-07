from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    TextField,
    HiddenField,
    PasswordField,
)

class IncomeCreateForm(BaseForm):
    title = TextField('Income Title',
                      [validators.Length(min=3, max=255)],
                      filters=[strip_filter])

class IncomeEditForm(IncomeCreateForm):
    id = HiddenField()
