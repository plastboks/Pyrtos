from pyrtos.forms.meta import BaseForm, strip_filter

from wtforms import (
    validators,
    TextField,
    HiddenField,
    BooleanField,
    PasswordField,
    SelectField,
)

from pyrtos.models import User


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
                                                 message='Passwords\
                                                          must match')],
                             filters=[strip_filter])
    confirm = PasswordField('Confirm password',
                            filters=[strip_filter])
    group = SelectField('Group',
                        choices=[(n, n) for n in User.groups])
    blocked = BooleanField('Blocked')


class UserEditForm(UserCreateForm):
    password = PasswordField('Password',
                             [validators.Optional(),
                              validators.Length(min=6, max=128),
                              validators.EqualTo('confirm',
                                                 message='Passwords\
                                                          must match')],
                             filters=[strip_filter])
    id = HiddenField()
