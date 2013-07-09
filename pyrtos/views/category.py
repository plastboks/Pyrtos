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
    Category,
)
from pyrtos.forms import (
    CategoryCreateForm,
    CategoryEditForm,
)

class CategoryViews(object):

    def __init__(self,request):
        self.request = request

    @view_config(route_name='categories',
                 renderer='pyrtos:templates/category/list.mako',
                 permission='view')
    def categories(self):
        page = int (self.request.params.get('page', 1))
        categories = Category.page(self.request, page)
        return {'paginator': categories,
                'title' : 'Shared categories',
                'archived' : False}

    @view_config(route_name='categories_private',
                 renderer='pyrtos:templates/category/list.mako',
                 permission='view')
    def categories_private(self):
        page = int (self.request.params.get('page', 1))
        categories = Category.page(self.request, page, private=True)
        return {'paginator': categories,
                'title' : 'Private categories',
                'archived' : False}

    @view_config(route_name='categories_archived',
                 renderer='pyrtos:templates/category/list.mako',
                 permission='view')
    def categories_archived(self):
        page = int (self.request.params.get('page', 1))
        categories = Category.page(self.request, page, archived=True)
        return {'paginator': categories,
                'title' : 'Archived categories',
                'archived' : True,}

    @view_config(route_name='category_new',
                 renderer='pyrtos:templates/category/edit.mako',
                 permission='create')
    def category_create(self):
        form = CategoryCreateForm(self.request.POST, csrf_context=self.request.session)
        if self.request.method == 'POST' and form.validate():
            c = Category()
            form.populate_obj(c)
            c.user_id = authenticated_userid(self.request)
            DBSession.add(c)
            self.request.session.flash('Category %s created' % (c.title), 'success')
            return HTTPFound(location=self.request.route_url('categories'))
        return {'title': 'New category',
                'form': form,
                'action': 'category_new'}

    @view_config(route_name='category_edit',
                 renderer='pyrtos:templates/category/edit.mako',
                 permission='edit')
    def category_edit(self):
        id = int(self.request.matchdict.get('id'))
        c = Category.by_id(id)
        if not c:
            return HTTPNotFound()
        if c.private and c.user_id is not authenticated_userid(self.request):
            return HTTPForbidden()
        form = CategoryEditForm(self.request.POST, c, csrf_context=self.request.session)
        if self.request.method == 'POST' and form.validate():
            form.populate_obj(c)
            self.request.session.flash('Category %s updated' % (c.title), 'status')
            return HTTPFound(location=self.request.route_url('categories'))
        return {'title' : 'Edit category',
                'form' : form,
                'id' : id,
                'action' : 'category_edit'}

    @view_config(route_name='category_archive',
                 renderer='string',
                 permission='archive')
    def category_archive(self):
        id = int(self.request.matchdict.get('id'))
        c = Category.by_id(id)
        if not c:
            return HTTPNotFound()
        if c.private and c.user_id is not authenticated_userid(self.request):
            return HTTPForbidden()
        c.archived = True
        DBSession.add(c)
        self.request.session.flash('Category %s archived' % (c.title), 'status')
        return HTTPFound(location=self.request.route_url('categories'))

    @view_config(route_name='category_restore',
                 renderer='string',
                 permission='restore')
    def category_restore(self):
        id = int(self.request.matchdict.get('id'))
        c = Category.by_id(id)
        if not c:
            return HTTPNotFound()
        if c.private and c.user_id is not authenticated_userid(self.request):
            return HTTPForbidden()
        c.archived = False
        DBSession.add(c)
        self.request.session.flash('Category %s restored' % (c.title), 'status')
        return HTTPFound(location=self.request.route_url('categories_archived'))

