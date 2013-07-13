from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    TextField,
    FloatField,
    DateField,
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
                      [validators.Length(min=2, max=255)],
                      filters=[strip_filter])
    amount = FloatField('Invoice Amount')
    due = DateField('Due date', format='%Y-%m-%d')
    paid = DateField('Paid date',
                     [validators.optional()],
                     format='%Y-%m-%d')
    category_id = QuerySelectField('Category',
                                    get_label='title')
    creditor_id = QuerySelectField('Creditor',
                                    get_label='title')

class InvoiceEditForm(InvoiceCreateForm):
    id = HiddenField()

class InvoiceSearchForm(BaseForm):
    query = TextField('Search',
                      [validators.Length(min=2, max=255)],
                      filters=[strip_filter])
