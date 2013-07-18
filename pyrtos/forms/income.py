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


class IncomeCreateForm(BaseForm):
    """
    Class constants representing form fields.

    title -- category tilte
    amount -- expenditure amount, as float
    user_id -- foregin key, this field is populated
               in the view file
    """
    title = TextField('Income Title',
                      [validators.Length(min=3, max=255)],
                      filters=[strip_filter])
    amount = FloatField('Income Amount')
    user_id = QuerySelectField('User',
                               get_label='email')


class IncomeEditForm(IncomeCreateForm):
    """
    Class constants representing form fields.

    id -- category id, used in edit forms.
    """
    id = HiddenField()
