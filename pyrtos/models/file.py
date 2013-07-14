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
    desc,
    asc,
)

from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True, nullable=False)
    filename = Column(String(255), unique=True, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    @classmethod
    def all_active(cls):
        return DBSession.query(File)

    @classmethod
    def by_id(cls, id):
        return DBSession.query(File).filter(File.id == id).first()

    @classmethod
    def page(cls, request, page):
        page_url = PageURL_WebOb(request)
        return Page(File.all_active(),
                    page,
                    url=page_url,
                    items_per_page=IPP)
