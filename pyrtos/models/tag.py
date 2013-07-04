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
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    @classmethod
    def popular(cls):
        return DBSession.query(Tag).get(20)

