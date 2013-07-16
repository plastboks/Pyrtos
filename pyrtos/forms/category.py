from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    TextField,
    HiddenField,
    PasswordField,
    BooleanField,
)

class CategoryCreateForm(BaseForm):
    title = TextField('Category Title',
                      [validators.Length(min=3, max=255)],
                      filters=[strip_filter])
    private = BooleanField('Private', default=False)

class CategoryEditForm(CategoryCreateForm):
    id = HiddenField()
