from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    TextField,
    HiddenField,
    PasswordField,
    BooleanField,
)


class CategoryCreateForm(BaseForm):
    """
    Class constants representing form fields.

    title -- category tilte
    private -- category boolean field
    """
    title = TextField('Category Title',
                      [validators.Length(min=3, max=255)],
                      filters=[strip_filter])
    private = BooleanField('Private', default=False)


class CategoryEditForm(CategoryCreateForm):
    """
    Class constants representing form fields.

    id -- category id, used in edit forms.
    """
    id = HiddenField()
