from pyrtos.models.meta import (
    DBSession,
    Base,
    IPP,
)

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    Unicode,
    UnicodeText,
    DateTime,
    Boolean,
    ForeignKey,
    or_,
    and_,
    )


from cryptacular.bcrypt import BCRYPTPasswordManager

from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words


class User(Base):
    """
    Class constants representing database table and its columns.

    id -- integer, primary key
    email -- string, unique, max 255 characters.
    givenname -- string, max 255 characters.
    surname -- string, max 255 characters.
    password -- string, bcrypt, max 255 characters.
    group -- string, max 10 charaters.
    archived -- boolean.
    blocked -- boolean.
    updated -- datetime.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    cellphone = Column(Integer, nullable=True)
    givenname = Column(String(255))
    surname = Column(String(255))
    password = Column(String(255), nullable=False)
    group = Column(String(10), nullable=False)
    archived = Column(Boolean, default=False)
    blocked = Column(Boolean, default=False)
    last_logged = Column(DateTime, default=datetime.utcnow)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.utcnow)

    """ Class constant used for accessing Bcrypt password manager. """
    pm = BCRYPTPasswordManager()

    """ Some usergroups. This is supposed to be improved sometime
    in the future.
    """
    groups = ['admin', 'editor', 'viewer']

    """ Method for returning a user based on id.

    id -- int, user id.
    """
    @classmethod
    def by_id(cls, id):
        return DBSession.query(User).filter(User.id == id).first()

    """ Method for returning a user based on email.
    We can do this, because the email column in the database is set as unique.

    email -- string, email.
    """
    @classmethod
    def by_email(cls, email):
        return DBSession.query(User).filter(User.email == email).first()

    """ Method for returning all rows in the table. Use with caution. """
    @classmethod
    def all_users(cls):
        return DBSession.query(User).all()

    """ Method for returning all rows with archived not set. """
    @classmethod
    def all_active(cls):
        return DBSession.query(User).filter(User.archived == False)

    """ Method for returning all rows with archived. """
    @classmethod
    def all_archived(cls):
        return DBSession.query(User).filter(User.archived == True)

    """ Pagination method for returning slices based on page id.

    request -- request object.
    page --int, page id.
    archived -- boolean.
    """
    @classmethod
    def page(cls, request, page, archived=False):
        page_url = PageURL_WebOb(request)
        if archived:
            return Page(User.all_archived(),
                        page,
                        url=page_url,
                        items_per_page=IPP)
        return Page(User.all_active(),
                    page,
                    url=page_url,
                    items_per_page=IPP)

    """ Method for checking object password against string.

    password -- string.
    """
    def verify_password(self, password):
        return self.pm.check(self.password, password)
