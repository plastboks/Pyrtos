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
    """
    Class constants representing form fields.

    title -- category tilte
    private -- category boolean field
    file -- fileupload filed
    """
    title = TextField('File Title',
                      [validators.Length(min=3, max=255)],
                      filters=[strip_filter])
    private = BooleanField('Private', default=False)
    file = FileField(u'File',
                     # add validation here
                     )


class FileEditForm(FileCreateForm):
    """
    Class constants representing form fields.

    id -- category id, used in edit forms.
    """
    id = HiddenField()
