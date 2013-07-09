from datetime import datetime
from slugify import slugify
from pyramid.response import Response
from sqlalchemy.exc import DBAPIError

from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
)

from pyramid.view import (
    view_config,
)
from pyramid.security import authenticated_userid
from pyrtos.models.meta import DBSession
from pyrtos.models import (
    Creditor,
)
from pyrtos.forms import (
    CreditorCreateForm,
    CreditorEditForm,
)

class CreditorViews(object):

    def __init__(self,request):
        self.request = request

    @view_config(route_name='creditors',
                 renderer='pyrtos:templates/creditor/list.mako',
                 permission='view')
    def creditors(self):
        page = int (self.request.params.get('page', 1))
        creditors = Creditor.page(self.request, page)
        return {'paginator': creditors,
                'title' : 'Public creditors',
                'archived' : False}

    @view_config(route_name='creditors_private',
                 renderer='pyrtos:templates/creditor/list.mako',
                 permission='view')
    def creditors_private(self):
        page = int (self.request.params.get('page', 1))
        creditors = Creditor.page(self.request, page, private=True)
        return {'paginator': creditors,
                'title' : 'Private creditors',
                'archived' : False}

    @view_config(route_name='creditors_archived',
                 renderer='pyrtos:templates/creditor/list.mako',
                 permission='view')
    def creditors_archived(self):
        page = int (self.request.params.get('page', 1))
        creditors = Creditor.page(self.request, page, archived=True)
        return {'paginator': creditors,
                'title' : 'Archived creditors',
                'archived' : True,}

    @view_config(route_name='creditor_new',
                 renderer='pyrtos:templates/creditor/edit.mako',
                 permission='create')
    def creditor_create(self):
        form = CreditorCreateForm(self.request.POST, csrf_context=self.request.session)
        if self.request.method == 'POST' and form.validate():
            c = Creditor()
            form.populate_obj(c)
            c.user_id = authenticated_userid(self.request)
            DBSession.add(c)
            self.request.session.flash('Creditor %s created' % (c.title), 'success')
            return HTTPFound(location=self.request.route_url('creditors'))
        return {'title': 'New creditor',
                'form': form,
                'action': 'creditor_new'}

    @view_config(route_name='creditor_edit',
                 renderer='pyrtos:templates/creditor/edit.mako',
                 permission='edit')
    def creditor_edit(self):
        id = int(self.request.matchdict.get('id'))
        c = Creditor.by_id(id)
        if not c:
            return HTTPNotFound()
        form = CreditorEditForm(self.request.POST, c, csrf_context=self.request.session)
        if self.request.method == 'POST' and form.validate():
            form.populate_obj(c)
            self.request.session.flash('Creditor %s updated' % (c.title), 'status')
            return HTTPFound(location=self.request.route_url('creditors'))
        return {'title' : 'Edit creditor',
                'form' : form,
                'id' : id,
                'action' : 'creditor_edit'}

    @view_config(route_name='creditor_archive',
                 renderer='string',
                 permission='archive')
    def creditor_archive(self):
        id = int(self.request.matchdict.get('id'))
        c = Creditor.by_id(id)
        if not c:
            return HTTPNotFound()
        c.archived = True
        DBSession.add(c)
        self.request.session.flash('Creditor %s archived' % (c.title), 'status')
        return HTTPFound(location=self.request.route_url('creditors'))

    @view_config(route_name='creditor_restore',
                 renderer='string',
                 permission='restore')
    def creditor_restore(self):
        id = int(self.request.matchdict.get('id'))
        c = Creditor.by_id(id)
        if not c:
            return HTTPNotFound()
        c.archived = False
        DBSession.add(c)
        self.request.session.flash('Creditor %s restored' % (c.title), 'status')
        return HTTPFound(location=self.request.route_url('creditors_archived'))
