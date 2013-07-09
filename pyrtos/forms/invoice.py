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


class InvoiceCreateForm(BaseForm):
    title = TextField('Invoice Title',
                      [validators.Length(min=3, max=255)],
                      filters=[strip_filter])
    amount = FloatField('Invoice Amount')
    category_id = QuerySelectField('Category',
                                    get_label='title')
    creditor_id = QuerySelectField('Creditor',
                                    get_label='title')

class InvoiceEditForm(InvoiceCreateForm):
    id = HiddenField()