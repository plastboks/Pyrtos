import os
import hashlib
import shutil
import mimetypes

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
    not_,
    desc,
    asc,
)

from sqlalchemy.orm import relationship
from pyrtos.security import authenticated_userid

from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words


class File(Base):
    """
    Class constants representing database table and its columns.

    id -- integer, primary key
    user_id -- integer, foreginkey. required.
    title -- string, 255 characters.
    filename -- string, 255 characters.
    filemime -- string, 32 characters.
    private -- boolean, default false.
    archived -- boolean, default false.
    created -- datetime.
    updated -- datetime.
    """
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    filename = Column(String(255), unique=True)
    filemime = Column(String(32))
    private = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    """ Constant used for getting this class foregin objects"""
    user = relationship('User', backref='files')

    """ Get all rows except what the user cannot access.

    request -- request object.
    """
    @classmethod
    def all_active(cls, request):
        id = authenticated_userid(request)
        return DBSession.query(File)\
                        .filter(File.archived == False)\
                        .filter(not_(and_(File.private == True,
                                          File.user_id != id)))

    """ Get all rows that has been marked as archived.

    request -- request object.
    """
    @classmethod
    def all_archived(cls, request):
        id = authenticated_userid(request)
        return DBSession.query(File)\
                        .filter(File.archived == True)\
                        .filter(not_(and_(File.private == True,
                                          File.user_id != id)))

    """ Page method used for lists with pagination.

    request -- request object.
    page -- integer.
    archived -- boolean.
    """
    @classmethod
    def page(cls, request, page, archived=False):
        page_url = PageURL_WebOb(request)
        if archived:
            return Page(File.all_archived(request),
                        page,
                        url=page_url,
                        items_per_page=IPP)
        return Page(File.all_active(request),
                    page,
                    url=page_url,
                    items_per_page=IPP)

    """ Get one record based on id.

    id -- integer.
    """
    @classmethod
    def by_id(cls, id):
        return DBSession.query(File).filter(File.id == id).first()

    """ Method used for creating uniform filenames.

    filename -- string.
    """
    def make_filename(self, filename):
        tmp_fileparts = os.path.splitext(filename)
        final_filename = hashlib.sha1(tmp_fileparts[0])\
                                .hexdigest()+tmp_fileparts[1]
        return final_filename

    """ Method for guessing mimetype, based on inputfilename.

    filename -- string.
    """
    def guess_mime(self, filename):
        return mimetypes.guess_type(filename)[0]

    """ Method for writing file to filesystem.

    input_file -- fileobject from post request.
    """
    def write_file(self, input_file):
        file_path = os.path.join('pyrtos/uploads', self.filename)
        with open(file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)
