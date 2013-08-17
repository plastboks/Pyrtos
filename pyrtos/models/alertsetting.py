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


class AlertSetting(Base):
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
    __tablename__ = 'alertsettings'
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
    active = Column(Boolean, default=True)
    archived = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.utcnow)

    """ Constants for relationships. """
    user = relationship('User', backref='alertsettings')
    weekfilter = relationship('WeekFilter',
                              backref='alertsetting',
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

    """ Method for getting one alertsetting by ID.

    id -- int, alertsetting id.
    """
    @classmethod
    def by_id(cls, uid, nid):
        return DBSession.query(AlertSetting)\
                        .join(AlertSetting.weekfilter)\
                        .filter(AlertSetting.id == nid)\
                        .filter(AlertSetting.user_id == uid)\
                        .first()

    """ Method for getting alertsettings for user.

    request -- request object.
    archived -- boolean, archived
    """
    @classmethod
    def my(cls, request, archived=False):
        id = authenticated_userid(request)
        if archived:
            return DBSession.query(AlertSetting)\
                            .join(AlertSetting.weekfilter)\
                            .filter(AlertSetting.user_id == id)\
                            .filter(AlertSetting.archived == True)
        return DBSession.query(AlertSetting)\
                        .join(AlertSetting.weekfilter)\
                        .filter(AlertSetting.user_id == id)\
                        .filter(AlertSetting.archived == False)

    """ Page method used for lists with pagination.

    request -- request object.
    page -- int, page int.
    archived -- boolean, archived
    """
    @classmethod
    def page(cls, request, page, archived=False):
        page_url = PageURL_WebOb(request)
        if archived:
            return Page(AlertSetting.my(request, archived=True),
                        page,
                        url=page_url,
                        items_per_page=IPP)
        return Page(AlertSetting.my(request),
                    page,
                    url=page_url,
                    items_per_page=IPP)
