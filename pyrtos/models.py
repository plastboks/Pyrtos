from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import (
    Column,
    Integer,
    Text,
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

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


##############
# User Class #
##############
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(255), unique=True, nullable=False)
    email = Column(Unicode(255), unique=True, nullable=False)
    givenname = Column(Unicode(255))
    surname = Column(Unicode(255))
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.utcnow)
   
    pm = BCRYPTPasswordManager()

    @classmethod
    def by_id(cls, id):
        return DBSession.query(User).filter(User.id == id).first()

    @classmethod
    def by_email(cls, email):
        return DBSession.query(User).filter(User.email == email).first()

    def verify_password(self, password):
        return self.pm.chech(self.password, password)

    def hash_password(self, password):
        return self.pm.encode(password)
