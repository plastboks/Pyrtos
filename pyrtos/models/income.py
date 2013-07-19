from pyrtos.models.meta import (
    DBSession,
    Base,
    IPP,
)

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    Float,
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
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words


class Income(Base):
    """
    Class constants representing database table and its columns.

    id -- integer, primary key
    user_id -- integer, foreginkey. required.
    title -- string, 255 characters.
    amount -- float, 16 characters.
    archived -- boolean, default false.
    created -- datetime.
    updated -- datetime.
    """
    __tablename__ = 'incomes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    amount = Column(Float(16), nullable=False)
    archived = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    """ Constant used for getting this class foregin objects"""
    user = relationship('User', backref='incomes')

    """ Get all rows except what the user cannot access.

    request -- request object.
    """
    @classmethod
    def all_active(cls):
        return DBSession.query(Income).filter(Income.archived == False)

    """ Get all rows that has been marked as archived.

    request -- request object.
    """
    @classmethod
    def all_archived(cls):
        return DBSession.query(Income).filter(Income.archived == True)

    """ Page method used for lists with pagination.

    request -- request object.
    page -- integer.
    archived -- boolean.
    """
    @classmethod
    def page(cls, request, page, archived=False):
        page_url = PageURL_WebOb(request)
        if archived:
            return Page(Income.all_archived(),
                        page,
                        url=page_url,
                        items_per_page=IPP)
        return Page(Income.all_active(),
                    page,
                    url=page_url,
                    items_per_page=IPP)

    """ Get one record based on id.

    id -- integer.
    """
    @classmethod
    def by_id(cls, id):
        return DBSession.query(Income).filter(Income.id == id).first()

    """ Method for return only sum for query. """
    @classmethod
    def amount_sum(cls):
        return DBSession.query(func.sum(Income.amount).label('a_sum'))\
                        .filter(Income.archived == False).first()
