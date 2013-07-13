import calendar
from pyrtos.models.meta import (
    DBSession,
    Base,
    IPP,
)

from pyrtos.models import Category

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
    not_,
    extract,
    )
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from pyramid.security import authenticated_userid

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
    def all_archived(cls, id):
        return DBSession.query(Invoice)\
                        .join(Invoice.category)\
                        .filter(Invoice.archived == True)\
                        .filter(not_(and_(Category.private == True,
                                          Category.user_id != id)))


    @classmethod
    def all_queryed(cls, id, q=False):
        base = DBSession.query(Invoice)\
                        .join(Invoice.category)\
                        .filter(not_(and_(Category.private == True,
                                          Category.user_id != id)))
        if q:
            q = "%"+q+"%"
            base.filter(Category.title.like(q))
        return base

    @classmethod
    def with_category_paid(cls, cid, year, month, total_only=False):
        if total_only:
            return DBSession.query(func.sum(Invoice.amount).label('a_sum'))\
                            .filter(and_(Invoice.archived == False,
                                         Invoice.category_id == cid,
                                         Invoice.paid != None,
                                        ))\
                            .filter(extract('year', Invoice.due) == year)\
                            .filter(extract('month', Invoice.due) == month)\
                            .first()

        return DBSession.query(Invoice)\
                        .filter(and_(Invoice.category_id == cid,
                                     Invoice.archived == False,
                                     Invoice.paid != None))\
                        .filter(extract('year', Invoice.due) == year)\
                        .filter(extract('month', Invoice.due) == month)\
                        .all()

    @classmethod
    def with_category_all_unpaid(cls, cid, total_only=False):
        if total_only:
            return DBSession.query(func.sum(Invoice.amount).label('a_sum'))\
                            .filter(and_(Invoice.archived == False,
                                         Invoice.category_id == cid,
                                         Invoice.paid == None,
                                        ))\
                            .first()

        return DBSession.query(Invoice)\
                        .filter(and_(Invoice.category_id == cid,
                                     Invoice.archived == False,
                                     Invoice.paid == None,
                                    ))\
                        .all()

    @classmethod
    def page(cls, request, page, archived=False):
        id = authenticated_userid(request)
        page_url = PageURL_WebOb(request)
        if archived:
            return Page(Invoice.all_archived(id),
                        page,
                        url=page_url,
                        items_per_page=IPP)
    
    @classmethod
    def searchpage(cls, request, page, qry=False):
        id = authenticated_userid(request)
        page_url = PageURL_WebOb(request)
        if qry:
            return Page(Invoice.all_queryed(id, q=qry),
                        page,
                        url=page_url,
                        items_per_page=IPP)
        return Page(Invoice.all_queryed(id),
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
