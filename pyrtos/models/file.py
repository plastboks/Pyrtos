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


class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True, nullable=False)
    filename = Column(String(255), unique=True, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    @classmethod
    def by_id(cls, id):
        return DBSession.query(File).filter(File.id == id).first()

