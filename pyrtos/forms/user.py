from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    TextField,
    HiddenField,
    PasswordField,
)

class UserCreateForm(BaseForm):
    email = TextField('Email',
                      [validators.Length(max=255),
                       validators.Email(message='Not an valid email address')],
                      filters=[strip_filter])
    givenname = TextField('Givenname',
                      [validators.Length(max=255)],
                      filters=[strip_filter])
    surname = TextField('Surname',
                      [validators.Length(max=255)],
                      filters=[strip_filter])
    password = PasswordField('Password',
                            [validators.Length(min=6, max=128),
                             validators.EqualTo('confirm',
                                                message='Passwords must match')],
                            filters=[strip_filter])
    confirm = PasswordField('Confirm password',
                            filter=[strip_filter])

class UserEditForm(UserCreateForm):
    id = HiddenField()
