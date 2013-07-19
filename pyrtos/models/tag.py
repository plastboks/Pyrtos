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


class Tag(Base):
    """
    Class constants representing database table and its columns.

    id -- integer, primary key
    name -- string, max 255 characters.
    created -- datetime.
    updated -- datetime.
    """
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    """ Dummy method for getting the most popular tags.
    This method is pr now done.
    """
    @classmethod
    def popular(cls):
        return DBSession.query(Tag).get(20)

    """ Method for getting one tag by ID.

    id -- int, tag id.
    """
    @classmethod
    def by_id(cls, id):
        return DBSession.query(Tag).filter(Tag.id == id).first()
