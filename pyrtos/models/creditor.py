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
from pyramid.security import authenticated_userid

from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words


class Creditor(Base):
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
    __tablename__ = 'creditors'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255))
    private = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.utcnow)

    """ Constant used for getting this class foregin objects"""
    user = relationship('User', backref='creditors')

    """ Get first row in table. Used for existence check"""
    @classmethod
    def first_active(cls):
        return DBSession.query(Creditor)\
                        .filter(and_(Creditor.archived == False,
                                     Creditor.private == False)).first()

    """ Get first row in table. Used for existence check.

    request -- request object.
    """
    @classmethod
    def first_private(cls, request):
        id = authenticated_userid(request)
        return DBSession.query(Creditor)\
                        .filter(and_(Creditor.archived == False,
                                     Creditor.private == True,
                                     Creditor.user_id == id)).first()

    """ Get all rows except what the user cannot access.

    request -- request object.
    id -- int, user id if request object is incomplete.
    """
    @classmethod
    def all_active(cls, request, id=False):
        if not id:
            id = authenticated_userid(request)
        return DBSession.query(Creditor)\
                        .filter(Creditor.archived == False)\
                        .filter(not_(and_(Creditor.private == True,
                                          Creditor.user_id != id)))

    """ Get all rows that has no special arguments"""
    @classmethod
    def all_shared(cls):
        return DBSession.query(Creditor)\
                        .filter(Creditor.archived == False)\
                        .filter(Creditor.private == False)

    """ Get all rows that has been marked as archived.

    request -- request object.
    """
    @classmethod
    def all_archived(cls, request):
        id = authenticated_userid(request)
        return DBSession.query(Creditor)\
                        .filter(Creditor.archived == True)\
                        .filter(not_(and_(Creditor.private == True,
                                          Creditor.user_id != id)))

    """ Get all rows that has been marked as private.

    request -- request object.
    """
    @classmethod
    def all_private(cls, request):
        id = authenticated_userid(request)
        return DBSession.query(Creditor)\
                        .filter(and_(Creditor.user_id == True,
                                     Creditor.private == True,
                                     Creditor.archived == False))

    """ Page method used for lists with pagination.

    request -- request object.
    page -- int, page id.
    archived -- boolean.
    """
    @classmethod
    def page(cls, request, page, archived=False):
        page_url = PageURL_WebOb(request)
        if archived:
            return Page(Creditor.all_archived(request),
                        page,
                        url=page_url,
                        items_per_page=IPP)
        return Page(Creditor.all_active(request),
                    page,
                    url=page_url,
                    items_per_page=IPP)

    """ Get one record based on id.

    id -- int, creditor id.
    """
    @classmethod
    def by_id(cls, id):
        return DBSession.query(Creditor).filter(Creditor.id == id).first()
