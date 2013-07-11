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
from webhelpers.date import (
  distance_of_time_in_words,
  time_ago_in_words,
)


class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    creditor_id = Column(Integer, ForeignKey('creditors.id'), nullable=False)
    title = Column(String(255), nullable=False)
    amount = Column(Float(16), nullable=False)
    due = Column(DateTime, nullable=False)
    paid = Column(DateTime, default=None)
    archived = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', backref='invoices')
    category = relationship('Category', backref='invoices')
    creditor = relationship('Creditor', backref='invoices')

    @classmethod
    def all_archived(cls):
        return DBSession.query(Invoice)\
                        .filter(Invoice.archived == True)

    @classmethod
    def with_category(cls, id, total_only=False, paid=False):
        if total_only:
            return DBSession.query(func.sum(Invoice.amount).label('a_sum'))\
                            .filter(and_(Invoice.archived == False,
                                         Invoice.category_id == id)).first()
        if paid:
            return DBSession.query(Invoice)\
                            .filter(and_(Invoice.category_id == id,
                                         Invoice.archived == False,
                                         Invoice.paid != None)).all()
        return DBSession.query(Invoice)\
                        .filter(and_(Invoice.category_id == id,
                                     Invoice.archived == False,
                                     Invoice.paid == None)).all()

    @classmethod
    def page(cls, request, page, archived=False):
        page_url = PageURL_WebOb(request)
        if archived:
            return Page(Invoice.all_archived(),
                        page,
                        url=page_url,
                        items_per_page=IPP)
    
    @classmethod
    def by_id(cls, id):
        return DBSession.query(Invoice).filter(Invoice.id == id).first()


    def time_to_expires_in_words(self):
      distance =  distance_of_time_in_words(from_time=self.due,
                                            to_time=datetime.utcnow(),
                                            round=True,
                                            granularity='day')
      if datetime.utcnow() > self.due:
          return 'Expired by: '+distance
      return 'In: '+distance

    def css_class_for_time_distance(self):
      distance =  distance_of_time_in_words(from_time=self.due,
                                            to_time=datetime.utcnow(),
                                            round=True,
                                            granularity='day')
      if datetime.utcnow() > self.due:
          return 'expired'
      return 'd'+distance.split(' ')[0]
