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
  email = Column(Unicode(255), unique=True, nullable=False)
  givenname = Column(Unicode(255))
  surname = Column(Unicode(255))
  last_logged = Column(DateTime, default=datetime.utcnow)
 
  pm = BCRYPTPasswordManager()


