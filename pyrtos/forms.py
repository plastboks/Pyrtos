from datetime import timedelta
from wtforms import (
    Form,
    validators,
    BooleanField,
    TextField,
    TextAreaField,
    HiddenField,
    PasswordField,
)

from wtforms.ext.csrf.session import SessionSecureForm

strip_filter = lambda x: x.strip() if x else None

class BaseForm(SessionSecureForm):
    SECRET_KEY = 'WAFaf3wefaASDF23r2vaGAETasdfgae4QdsfWAEFWKYUJH'
    TIME_LIMIT = timedelta(minutes=30)

class LoginForm(BaseForm):
    email = TextField('Email',
                      [validators.Length(min=4, max=255),
                       validators.Email(message='Not an valid email address')],
                       filters=[strip_filter])
    password = PasswordField('Password',
                             [validators.Length(min=5, max=255)],
                             filters=[strip_filter])

class CategoryCreateForm(BaseForm):
    name = TextField('Category Name',
                      [validators.Length(max=255)],
                      filters=[strip_filter])
    title = TextField('Category Title',
                      [validators.Length(max=255)],
                      filters=[strip_filter])

class CategoryEditForm(CategoryCreateForm):
    id = HiddenField()
