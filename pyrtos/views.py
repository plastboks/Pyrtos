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
)

from .models import (
    DBSession,
    User,
    )

#########
# Index #
#########
@view_config(route_name='index',
             renderer='pyrtos:templates/index.mako')
def index(request):
    return {'title': 'Hello world'}

################
# Login/logout #
################
@view_config(route_name='login',
             renderer='pyrtos:templates/login.mako')
@view_config(route_name='login',
             renderer='string',
             request_method='POST')
@forbidden_view_config(renderer='pyrtos:templates/login.mako')
def login(request):
    if request.method == 'POST' and request.POST.get('email'):
        user = User.by_email(request.POST.get('email'))
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.id)
            return HTTPFound(location=request.route_url('index'),
                             headers=headers)
        headers = forget(request)
        request.session.flash('Login failed')
        return HTTPFound(location=request.route_url('login'),
                         headers=headers)
    if authenticated_userid(request):
        return HTTPFound(location=request.route_url('index'))

    return {'action' : request.matchdict.get('action'),
            'title' : 'Login'}

@view_config(route_name='logout',
             renderer='string')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('login'),
                     headers=headers)
