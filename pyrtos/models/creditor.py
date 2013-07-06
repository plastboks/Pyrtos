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

from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words


class Creditor(Base):
    __tablename__ = 'creditors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    title = Column(String(255))
    archived = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    @classmethod
    def all_active(cls):
        return DBSession.query(Creditor).filter(Creditor.archived == False)

    @classmethod
    def all_archived(cls):
        return DBSession.query(Creditor).filter(Creditor.archived == True)

    @classmethod
    def page(cls, request, page, archived=False):
        page_url = PageURL_WebOb(request)
        if archived:
            return Page(Creditor.all_archived(), page, url=page_url, items_per_page=IPP)
        return Page(Creditor.all_active(), page, url=page_url, items_per_page=IPP)
    
    @classmethod
    def by_id(cls, id):
        return DBSession.query(Creditor).filter(Creditor.id == id).first()

    @classmethod
    def by_name(cls, name):
        return DBSession.query(Creditor).filter(Creditor.name == name).first()

