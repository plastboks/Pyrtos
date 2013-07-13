from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    widgets,
    TextField,
    FloatField,
    DateField,
    HiddenField,
    SelectField,
    PasswordField,
    SelectMultipleField,
)
from wtforms.ext.sqlalchemy.fields import (
    QuerySelectField,
    QuerySelectMultipleField,
)

from pyrtos.models import User

class MultiCheckboxField(QuerySelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

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
                      [validators.Length(max=255)],
                      filters=[strip_filter])

    categories = MultiCheckboxField('Categories',
                                    get_label='title')

    creditors = MultiCheckboxField('Creditors',
                                    get_label='title')
    fromdate = DateField('From date',
                     [validators.optional()],
                     format='%Y-%m-%d')
    todate = DateField('To date',
                     [validators.optional()],
                     format='%Y-%m-%d')
