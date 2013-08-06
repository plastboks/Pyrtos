from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    widgets,
    TextField,
    TextAreaField,
    FloatField,
    DateField,
    HiddenField,
    SelectField,
    PasswordField,
    SelectMultipleField,
    FileField,
    BooleanField,
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
    """
    Class constants representing form fields.

    title -- category tilte.
    amount -- expenditure amount, as float.
    due -- datefiled for invoice duedate.
    paid -- datefield for invoice paiddate.
    attachment -- filefield.
    category_id -- foreginkey. populated in view file
    creditor_id -- foreginkey. populated in view file
    on_hold -- booleanfield.
    """
    title = TextField('Title',
                      [validators.Length(min=2, max=255)],
                      filters=[strip_filter])
    notes = TextAreaField('Notes',
                          [validators.Length(max=2048)],
                          filters=[strip_filter])
    amount = FloatField('Amount')
    due = DateField('Due date', format='%Y-%m-%d')
    paid = DateField('Paid date',
                     [validators.optional()],
                     format='%Y-%m-%d')
    attachment = FileField('Attachment')
    category_id = QuerySelectField('Category',
                                   get_label='title')
    creditor_id = QuerySelectField('Creditor',
                                   get_label='title')
    on_hold = BooleanField('On hold')
    reminder_true = BooleanField('Reminder', default=True)


class InvoiceEditForm(InvoiceCreateForm):
    """
    Class constants representing form fields.

    id -- category id, used in edit forms.
    files -- foreignkey. populated in view files.
    """
    id = HiddenField()
    files = MultiCheckboxField('Files',
                               [validators.optional()],
                               get_label='title')


class InvoiceSearchForm(BaseForm):
    """
    Class constants representing form fields.

    query -- textfield, search query string.
    categories -- all categoires. populated in view file.
    creditors -- all creditors. populated in view file.
    fromdate -- datefield.
    todate -- datefiled.
    """
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
