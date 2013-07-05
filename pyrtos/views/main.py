from datetime import datetime
from pyramid.response import Response
from sqlalchemy.exc import DBAPIError

from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
)
from pyramid.security import (
    remember,
    forget,
    authenticated_userid
)
from pyramid.view import (
    view_config,
    forbidden_view_config,
    notfound_view_config,
)


class MainViews(object):
    
    def __init__(self,request):
        self.request = request

    @view_config(route_name='index',
                 renderer='pyrtos:templates/index.mako',
                 permission='view')
    def index(self):
        return {'title': 'Hello world'}

    @forbidden_view_config(renderer='string')
    def forbidden(self):
        return HTTPFound(self.request.route_url('login'))

    @notfound_view_config(renderer='pyrtos:templates/notfound.mako')
    def notfound(self):
        return {'title': '404 - Page not found',
                'message' : '"%s" is not the page you are looking for!' % self.request.path}
