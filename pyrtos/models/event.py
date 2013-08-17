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
    DateTime,
    Boolean,
    ForeignKey,
    not_,
    and_,
)

from sqlalchemy.orm import relationship
from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words
from pyramid.security import authenticated_userid


class Event(Base):
    """
    Class constants representing database table and its columns.

    id -- integer, primary key
    created -- datetime.
    updated -- datetime.
    """
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    reminder_id = Column(Integer, ForeignKey('reminders.id'))
    title = Column(String(255), nullable=False)
    private = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)
    from_date = Column(DateTime)
    to_date = Column(DateTime)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.utcnow)

    """ Foregin key variables"""
    user = relationship('User', backref='events')
    reminder = relationship('Reminder', backref='event')

    """ Get all rows except what the user cannot access

    request -- request object.
    """
    @classmethod
    def all_active(cls, request):
        uid = authenticated_userid(request)
        return DBSession.query(Event)\
                        .filter(Event.archived == False)\
                        .filter(not_(and_(Event.private == True,
                                          Event.user_id != uid)))

    """ Get all archived rows

    request -- request object.
    """
    @classmethod
    def all_archived(cls, request):
        uid = authenticated_userid(request)
        return DBSession.query(Event)\
                        .filter(Event.archived == True)\
                        .filter(not_(and_(Event.private == True,
                                          Event.user_id != uid)))

    """ Page method used for lists with pagination.

    request -- request object.
    page -- int, page int.
    """
    @classmethod
    def page(cls, request, page, archived=False):
        page_url = PageURL_WebOb(request)
        if archived:
            return Page(Event.all_archived(request),
                        page,
                        url=page_url,
                        items_per_page=IPP)
        return Page(Event.all_active(request),
                    page,
                    url=page_url,
                    items_per_page=IPP)

    """ Method for getting one tag by ID.

    id -- int, tag id.
    """
    @classmethod
    def by_id(cls, id):
        return DBSession.query(Event).filter(Event.id == id).first()
