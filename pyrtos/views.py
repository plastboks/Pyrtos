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
)

from .models import (
    DBSession,
    User,
    Category,
    )
from .forms import (
    CategoryCreateForm,
    CategoryEditForm,
)


#########
# Index #
#########
@view_config(route_name='index',
             renderer='pyrtos:templates/index.mako',
             permission='view')
def index(request):
    return {'title': 'Hello world'}


##############
# Categories #
##############
@view_config(route_name='categories',
             renderer='pyrtos:templates/category/list.mako',
             permission='view')
def categories(request):
    page = int (request.params.get('page', 1))
    categories = Category.page(request, page)
    return {'paginator': categories,
            'title' : 'Categories'}

@view_config(route_name='category_new',
             renderer='pyrtos:templates/category/edit.mako',
             permission='create')
def category_create(request):
    form = CategoryCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        c = Category()
        form.populate_obj(c)
        DBSession.add(c)
        request.session.flash('Category %s created' % (c.title))
        return HTTPFound(location=request.route_url('categories'))
    return {'title': 'New category',
            'form': form,
            'action': 'category_new'}

@view_config(route_name='category_edit',
             renderer='pyrtos:templates/category/edit.mako',
             permission='edit')
def category_edit(request):
    id = int(request.matchdict.get('id'))
    c = Category.by_id(id)
    if not c:
        return HTTPNotFound()
    form = CategoryEditForm(request.POST, c)
    if request.method == 'POST' and form.validate():
        form.populate_obj(c)
        request.session.flash('Category %s updated' % (c.title))
        return HTTPFound(location=request.route_url('categories'))
    return {'title' : 'Edit category',
            'form' : form,
            'id' : id,
            'action' : 'category_edit'}


################
# Login/logout #
################
@view_config(route_name='login',
             renderer='pyrtos:templates/login.mako')
@view_config(route_name='login',
             renderer='string',
             request_method='POST')
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


#############
# Forbidden #
#############
@forbidden_view_config(renderer='pyrtos:templates/login.mako')
def forbidden(request):
    return HTTPFound(request.route_url('login'))
