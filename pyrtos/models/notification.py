from pyrtos.models.meta import (
    DBSession,
    Base,
    IPP,
)

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    String,
    Boolean,
)

from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words
from pyramid.security import authenticated_userid
from sqlalchemy.orm import relationship


class Notification(Base):
    """
    Class constants representing database table and its columns.

    id -- integer, primary key
    user_id -- integer, foreign key to users
    method_id -- integer, foregin key to methods...
    hour -- integer, hour.
    minute -- integer, minute.
    created -- datetime.
    updated -- datetime.
    """
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    weekfilter_id = Column(Integer,
                           ForeignKey('weekfilters.id'),
                           nullable=False,
                           )
    title = Column(String(255), nullable=False)
    method = Column(Integer, default=0)
    hour = Column(Integer, nullable=False, default=0)
    minute = Column(Integer, nullable=False, default=0)
    days_in_advance = Column(Integer, default=0)
    archived = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    """ Constants for relationships. """
    weekfilter = relationship('WeekFilter',
                              backref='notification',
                              lazy='joined')

    """ Some nice lists."""
    hour_list = range(0, 24)
    minute_list = range(0, 60, 15)
    days_list = [('monday', 'Monday'),
                 ('tuesday', 'Tuesday'),
                 ('wednesday', 'Wednesday'),
                 ('thursday', 'Thursday'),
                 ('friday', 'Friday'),
                 ('saturday', 'Saturday'),
                 ('sunday', 'Sunday'),
                 ]
    days_advance_list = range(0, 5)

    """ Method for getting one notification by ID.

    id -- int, notification id.
    """
    @classmethod
    def by_id(cls, uid, nid):
        return DBSession.query(Notification)\
                        .join(Notification.weekfilter)\
                        .filter(Notification.id == nid)\
                        .filter(Notification.user_id == uid)\
                        .first()

    """ Method for getting notifications for user.

    request -- request object.
    """
    @classmethod
    def my(cls, request):
        id = authenticated_userid(request)
        return DBSession.query(Notification)\
                        .join(Notification.weekfilter)\
                        .filter(Notification.user_id == id)\

    """ Page method used for lists with pagination.

    request -- request object.
    page -- int, page int.
    """
    @classmethod
    def page(cls, request, page):
        page_url = PageURL_WebOb(request)
        return Page(Notification.my(request),
                    page,
                    url=page_url,
                    items_per_page=IPP)
