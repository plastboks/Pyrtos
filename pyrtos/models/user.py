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
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    givenname = Column(String(255))
    surname = Column(String(255))
    password = Column(String(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.utcnow)
   
    pm = BCRYPTPasswordManager()

    @classmethod
    def by_id(cls, id):
        return DBSession.query(User).filter(User.id == id).first()

    @classmethod
    def by_email(cls, email):
        return DBSession.query(User).filter(User.email == email).first()

    @classmethod
    def all(cls):
        return DBSession.query(User)

    @classmethod
    def page(cls, request, page):
        page_url = PageURL_WebOb(request)
        return Page(User.all(), page, url=page_url, items_per_page=IPP)
    
    def verify_password(self, password):
        return self.pm.check(self.password, password)
    
