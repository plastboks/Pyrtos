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

from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words

from pyramid.security import authenticated_userid

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255))
    private = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', backref='categories')

    @classmethod
    def all_active(cls):
        return DBSession.query(Category).filter(and_(Category.archived == False,
                                                     Category.private == False))

    @classmethod
    def all_archived(cls):
        return DBSession.query(Category).filter(Category.archived == True)

    @classmethod
    def all_private(cls, request):
        id = authenticated_userid(request)
        return DBSession.query(Category).filter(and_(Category.user_id == True,\
                                                     Category.private == True,\
                                                     Category.archived == False))

    @classmethod
    def page(cls, request, page, archived=False, private=False):
        page_url = PageURL_WebOb(request)
        if archived:
            return Page(Category.all_archived(), page, url=page_url, items_per_page=IPP)
        if private:
            return Page(Category.all_private(request), page, url=page_url, items_per_page=IPP)
        return Page(Category.all_active(), page, url=page_url, items_per_page=IPP)
    
    @classmethod
    def by_id(cls, id):
        return DBSession.query(Category).filter(Category.id == id).first()


