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


class ExpenditureCreateForm(BaseForm):
    """
    Class constants representing form fields.

    title -- category tilte
    amount -- expenditure amount, as float
    category_id -- foregin key, this field is populated
                   in the view file
    """
    title = TextField('Expenditure Title',
                      [validators.Length(min=3, max=255)],
                      filters=[strip_filter])
    amount = FloatField('Expenditure Amount')
    category_id = QuerySelectField('Category',
                                   get_label='title')


class ExpenditureEditForm(ExpenditureCreateForm):
    """
    Class constants representing form fields.

    id -- category id, used in edit forms.
    """
    id = HiddenField()
