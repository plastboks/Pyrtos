from datetime import timedelta

from wtforms.ext.csrf.session import SessionSecureForm

strip_filter = lambda x: x.strip() if x else None

class BaseForm(SessionSecureForm):
    SECRET_KEY = 'WAFaf3wefaASDF23r2vaGAETasdfgae4QdsfWAEFWKYUJH'
    TIME_LIMIT = timedelta(minutes=30)

