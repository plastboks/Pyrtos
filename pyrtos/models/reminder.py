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
)

from sqlalchemy.orm import relationship
from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words
from pyramid.security import authenticated_userid


class Reminder(Base):
    """
    Class constants representing database table and its columns.

    id -- integer, primary key
    name -- string, max 255 characters.
    created -- datetime.
    updated -- datetime.
    """
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
    alert = Column(DateTime)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    """ some lists. """
    types = {0: 'Onetime',
             1: 'Concurring',
             }

    """ Get all rows except what the user cannot access

    request -- request object.
    """
    @classmethod
    def all_active(cls, request):
        """ Dont do anything with the request object for now. """
        return DBSession.query(Reminder)\
                        .filter(Reminder.active == True)

    """ Get all rows except what the user cannot access

    request -- request object.
    """
    @classmethod
    def all_inactive(cls, request):
        """ Dont do anything with the request object for now. """
        return DBSession.query(Reminder)\
                        .filter(Reminder.active == False)

    """ Page method used for lists with pagination.

    request -- request object.
    page -- int, page int.
    """
    @classmethod
    def page(cls, request, page, inactive=False):
        page_url = PageURL_WebOb(request)
        if inactive:
            return Page(Reminder.all_inactive(request),
                        page,
                        url=page_url,
                        items_per_page=IPP)
        return Page(Reminder.all_active(request),
                    page,
                    url=page_url,
                    items_per_page=IPP)

    """ Method for getting one tag by ID.

    id -- int, tag id.
    """
    @classmethod
    def by_id(cls, id):
        return DBSession.query(Reminder).filter(Reminder.id == id).first()
