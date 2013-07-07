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
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    givenname = Column(String(255))
    surname = Column(String(255))
    password = Column(String(255), nullable=False)
    group = Column(String(10), nullable=False)
    archived = Column(Boolean, default=False)
    blocked = Column(Boolean, default=False)
    last_logged = Column(DateTime, default=datetime.utcnow)
   
    pm = BCRYPTPasswordManager()

    groups = ['admin', 'editor', 'viewer']

    @classmethod
    def by_id(cls, id):
        return DBSession.query(User).filter(User.id == id).first()

    @classmethod
    def by_email(cls, email):
        return DBSession.query(User).filter(User.email == email).first()

    @classmethod
    def all_users(cls):
        return DBSession.query(User).all()

    @classmethod
    def all_active(cls):
        return DBSession.query(User).filter(User.archived == False)

    @classmethod
    def all_archived(cls):
        return DBSession.query(User).filter(User.archived == True)

    @classmethod
    def page(cls, request, page, archived=False):
        page_url = PageURL_WebOb(request)
        if archived:
          return Page(User.all_archived(), page, url=page_url, items_per_page=IPP)
        return Page(User.all_active(), page, url=page_url, items_per_page=IPP)
    
    def verify_password(self, password):
        return self.pm.check(self.password, password)
    
