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
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    """ some lists. """
    types = ['onetime',
             'concuring',
             ]

    """ Method for getting one tag by ID.

    id -- int, tag id.
    """
    @classmethod
    def by_id(cls, id):
        return DBSession.query(Reminder).filter(Reminder.id == id).first()
