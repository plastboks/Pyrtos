from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    TextField,
    FloatField,
    HiddenField,
    SelectField,
    PasswordField,
)
from wtforms.ext.sqlalchemy.fields import (
    QuerySelectField,
)

from pyrtos.models import User

def users():
    return User.all_users()

class IncomeCreateForm(BaseForm):
    title = TextField('Income Title',
                      [validators.Length(min=3, max=255)],
                      filters=[strip_filter])
    amount = FloatField('Income Amount')
    user_id = QuerySelectField('User',
                                query_factory=users,
                                get_label='email')

class IncomeEditForm(IncomeCreateForm):
    id = HiddenField()
