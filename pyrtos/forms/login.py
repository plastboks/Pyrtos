from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    TextField,
    PasswordField,
)


class LoginForm(BaseForm):
    """
    Class constants representing form fields.

    email -- textfield. username.
    password -- textfield. password.
    """
    email = TextField('Email',
                      [validators.Length(min=4, max=255),
                       validators.Email(message='Not an valid email address')],
                      filters=[strip_filter])
    password = PasswordField('Password',
                             [validators.Length(min=5, max=255)],
                             filters=[strip_filter])
