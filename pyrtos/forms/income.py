from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    TextField,
    FloatField,
    HiddenField,
    SelectField,
    PasswordField,
)

from pyrtos.models import User

class IncomeCreateForm(BaseForm):
    title = TextField('Income Title',
                      [validators.Length(min=3, max=255)],
                      filters=[strip_filter])
    amount = FloatField('Income Amount')
    user_id = SelectField('User',
                          coerce=int,
                          choices=[(n.id,n.email) for n in User.all_users()])

class IncomeEditForm(IncomeCreateForm):
    id = HiddenField()
