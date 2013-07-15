from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    TextField,
    HiddenField,
    PasswordField,
    BooleanField,
    FileField,
)

class FileCreateForm(BaseForm):
    title = TextField('File Title',
                      [validators.Length(min=3, max=255)],
                      filters=[strip_filter])
    private = BooleanField('Private', default=False)
    file = FileField(u'File',
                     # add validation here
                     )

class FileEditForm(FileCreateForm):
    id = HiddenField()
