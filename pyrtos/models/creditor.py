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

from sqlalchemy.orm import relationship
from pyramid.security import authenticated_userid

from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words



class Creditor(Base):
    __tablename__ = 'creditors'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255))
    private = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', backref='creditors')

    @classmethod
    def first_active(cls):
        return DBSession.query(Creditor)\
                        .filter(and_(Creditor.archived == False,
                                     Creditor.private == False)).first()
    @classmethod
    def first_private(cls, request):
        id = authenticated_userid(request)
        return DBSession.query(Creditor)\
                        .filter(and_(Creditor.archived == False,\
                                     Creditor.private == True,\
                                     Creditor.user_id == id)).first()

    @classmethod
    def all_active(cls):
        return DBSession.query(Creditor)\
                        .filter(and_(Creditor.archived == False,
                                     Creditor.private == False))

    @classmethod
    def all_archived(cls):
        return DBSession.query(Creditor)\
                        .filter(Creditor.archived == True)

    @classmethod
    def all_private(cls, request):
        id = authenticated_userid(request)
        return DBSession.query(Creditor)\
                        .filter(and_(Creditor.user_id == True,\
                                     Creditor.private == True,\
                                     Creditor.archived == False))

    @classmethod
    def page(cls, request, page, archived=False, private=False):
        page_url = PageURL_WebOb(request)
        if archived:
            return Page(Creditor.all_archived(),
                        page,
                        url=page_url,
                        items_per_page=IPP)
        if private:
            return Page(Creditor.all_private(request),
                        page,
                        url=page_url,
                        items_per_page=IPP)
        return Page(Creditor.all_active(),
                    page,
                    url=page_url,
                    items_per_page=IPP)
    
    @classmethod
    def by_id(cls, id):
        return DBSession.query(Creditor).filter(Creditor.id == id).first()

