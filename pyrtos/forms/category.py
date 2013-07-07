from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    TextField,
    HiddenField,
    PasswordField,
)

class CategoryCreateForm(BaseForm):
    title = TextField('Category Title',
                      [validators.Length(min=3, max=255)],
                      filters=[strip_filter])

class CategoryEditForm(CategoryCreateForm):
    id = HiddenField()
