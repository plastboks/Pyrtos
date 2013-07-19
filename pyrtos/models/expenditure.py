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


class Expenditure(Base):
    """
    Class constants representing database table and its columns.

    id -- integer, primary key
    user_id -- integer, foreginkey. required.
    category_id -- integer, foreginkey. required.
    title -- string, 255 characters.
    amount -- float, 16 characters.
    archived -- boolean, default false.
    created -- datetime.
    updated -- datetime.
    """
    __tablename__ = 'expenditures'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    title = Column(String(255), nullable=False)
    amount = Column(Float(16), nullable=False)
    archived = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    """ Constant used for getting this class foregin objects"""
    user = relationship('User', backref='expenditures')
    """ Constant used for getting this class foregin objects"""
    category = relationship('Category', backref='expenditures')

    """ Get all rows that has been marked as archived"""
    @classmethod
    def all_archived(cls):
        return DBSession.query(Expenditure)\
                        .filter(Expenditure.archived == True)

    """ Get all rows with a certain category.

    id -- int, category id.
    total_only -- boolean.
    """
    @classmethod
    def with_category(cls, id, total_only=False):
        if total_only:
            return DBSession.query(func.sum(Expenditure.amount)
                                       .label('a_sum'))\
                            .filter(and_(Expenditure.archived == False,
                                         Expenditure.category_id == id))\
                            .first()
        return DBSession.query(Expenditure)\
                        .filter(and_(Expenditure.category_id == id,
                                     Expenditure.archived == False)).all()

    """ Page method used for lists with pagination.

    request -- request object.
    page -- int.
    archived -- boolean.
    """
    @classmethod
    def page(cls, request, page, archived=False):
        page_url = PageURL_WebOb(request)
        if archived:
            return Page(Expenditure.all_archived(),
                        page,
                        url=page_url,
                        items_per_page=IPP)

    """ Get one record based on id.

    id -- int, expenditure id.
    """
    @classmethod
    def by_id(cls, id):
        return DBSession.query(Expenditure)\
                        .filter(Expenditure.id == id).first()
