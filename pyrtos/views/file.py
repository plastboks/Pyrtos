from datetime import datetime
from slugify import slugify
from pyramid.response import Response
from sqlalchemy.exc import DBAPIError

from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
    HTTPForbidden,
)
from pyramid.security import (
    remember,
    forget,
    authenticated_userid
)
from pyramid.view import (
    view_config,
)
from pyrtos.models.meta import DBSession
from pyrtos.models import (
    File,
)

class FileViews(object):

    def __init__(self,request):
        self.request = request


    @view_config(route_name='files',
                 renderer='pyrtos:templates/file/list.mako',
                 permission='view')
    def files(self):
        page = int (self.request.params.get('page', 1))
        files = File.page(self.request, page)
        return {'paginator': files,
                'title' : 'Files',}

