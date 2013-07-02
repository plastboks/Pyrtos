from wtforms import (
    Form,
    validators,
    BooleanField,
    TextField,
    TextAreaField,
    HiddenField,
    PasswordField,
)

strip_filter = lambda x: x.strip() if x else None

class CategoryCreateForm(Form):
    name = TextField('Category Name',
                      [validators.Length(max=255)],
                      filters=[strip_filter])
    title = TextField('Category Title',
                      [validators.Length(max=255)],
                      filters=[strip_filter])

class CategoryEditForm(CategoryCreateForm):
    id = HiddenField()
