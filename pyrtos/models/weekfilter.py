from pyrtos.models.meta import (
    DBSession,
    Base,
    IPP,
)

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
)

from sqlalchemy.orm import relationship


class WeekFilter(Base):
    """
    Class constants representing database table and its columns.

    id -- integer, primary key
    monday -- boolean.
    tuesday -- boolean.
    wednesday -- boolean.
    thursday -- boolean.
    friday -- boolean.
    saturday -- boolean.
    sunday -- boolean.
    created -- datetime.
    updated -- datetime.
    """
    __tablename__ = 'weekfilters'
    id = Column(Integer, primary_key=True)
    monday = Column(Boolean, default=False)
    tuesday = Column(Boolean, default=False)
    wednesday = Column(Boolean, default=False)
    thursday = Column(Boolean, default=False)
    friday = Column(Boolean, default=False)
    saturday = Column(Boolean, default=False)
    sunday = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)
