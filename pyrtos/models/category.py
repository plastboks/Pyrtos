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
    not_,
    )

from sqlalchemy.orm import relationship

from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words

from pyramid.security import authenticated_userid


class Category(Base):
    """
    Class constants representing database table and its columns.

    id -- integer, primary key
    user_id -- integer, foreginkey. required.
    title -- string, 255 characters.
    private -- boolean, default false.
    archived -- boolean, default false.
    created -- datetime.
    updated -- datetime.
    """
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255))
    private = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.utcnow)

    """ Constant used for getting this class foregin objects"""
    user = relationship('User', backref='categories')

    """ Get first row in table. Used for existence check"""
    @classmethod
    def first_active(cls):
        return DBSession.query(Category)\
                        .filter(and_(Category.archived == False,
                                     Category.private == False)).first()

    """ Get first row in table. Used for existence check.

    request -- request object.
    """
    @classmethod
    def first_private(cls, request):
        id = authenticated_userid(request)
        return DBSession.query(Category)\
                        .filter(and_(Category.archived == False,
                                     Category.private == True,
                                     Category.user_id == id)).first()

    """ Get all rows except what the user cannot access

    request -- request object.
    id -- int, user id if the request object is not complete.
    """
    @classmethod
    def all_active(cls, request, id=False):
        if not id:
            id = authenticated_userid(request)
        return DBSession.query(Category)\
                        .filter(Category.archived == False)\
                        .filter(not_(and_(Category.private == True,
                                          Category.user_id != id)))

    """ Get all rows that has no special arguments"""
    @classmethod
    def all_shared(cls):
        return DBSession.query(Category)\
                        .filter(Category.archived == False)\
                        .filter(Category.private == False)

    """ Get all rows that has been marked as archived.

    request -- request object.
    """
    @classmethod
    def all_archived(cls, request):
        id = authenticated_userid(request)
        return DBSession.query(Category)\
                        .filter(Category.archived == True)\
                        .filter(not_(and_(Category.private == True,
                                          Category.user_id != id)))

    """ Get all rows that has been marked as private.

    request -- request object.
    id -- int, user id if request object is not complete.
    """
    @classmethod
    def all_private(cls, request, id=False):
        if not id:
            id = authenticated_userid(request)
        return DBSession.query(Category)\
                        .filter(and_(Category.user_id == id,
                                     Category.private == True,
                                     Category.archived == False))

    """ Page method used for lists with pagination.

    request -- request object.
    page -- int, page int.
    archived -- boolean.
    """
    @classmethod
    def page(cls, request, page, archived=False):
        page_url = PageURL_WebOb(request)
        if archived:
            return Page(Category.all_archived(request),
                        page,
                        url=page_url,
                        items_per_page=IPP)
        return Page(Category.all_active(request),
                    page,
                    url=page_url,
                    items_per_page=IPP)

    """ Get one record based on id.

    id -- int, category id.
    """
    @classmethod
    def by_id(cls, id):
        return DBSession.query(Category).filter(Category.id == id).first()
