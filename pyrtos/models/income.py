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
    __tablename__ = 'incomes'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    amount = Column(Float(16), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    archived = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', backref='incomes')

    @classmethod
    def all_active(cls):
        return DBSession.query(Income).filter(Income.archived == False)

    @classmethod
    def all_archived(cls):
        return DBSession.query(Income).filter(Income.archived == True)

    @classmethod
    def page(cls, request, page, archived=False):
        page_url = PageURL_WebOb(request)
        if archived:
            return Page(Income.all_archived(), page, url=page_url, items_per_page=IPP)
        return Page(Income.all_active(), page, url=page_url, items_per_page=IPP)
    
    @classmethod
    def by_id(cls, id):
        return DBSession.query(Income).filter(Income.id == id).first()

    @classmethod
    def amount_sum(cls):
        return DBSession.query(func.sum(Income.amount).label('a_sum')).\
                         filter(Income.archived == False).first()

