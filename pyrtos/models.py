from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    Unicode,
    UnicodeText,
    DateTime,
    ForeignKey,
    or_,
    and_,
    )

from cryptacular.bcrypt import BCRYPTPasswordManager
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

IPP = 12

##############
# User Class #
##############
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

    def verify_password(self, password):
        return self.pm.check(self.password, password)
    

##############
# Categories #
##############
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    title = Column(String(255))
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    @classmethod
    def all(cls):
        return DBSession.query(Category).order_by(sa.desc(Category.created))

    @classmethod
    def page(cls, request, page):
        page_url = PageURL_WebOb(request)
        return Page(Category.all(), page, url=page_url, items_per_page=IPP)
    
    @classmethod
    def by_name(cls, name):
        return DBSession.query(Category).filter(Category.name == name).first()
