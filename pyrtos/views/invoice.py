from datetime import datetime
from slugify import slugify
from pyramid.response import Response
from sqlalchemy.exc import DBAPIError

from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
)
from pyramid.security import (
    authenticated_userid
)
from pyramid.view import (
    view_config,
)
from pyrtos.models.meta import DBSession
from pyrtos.models import (
    Category,
    Invoice,
    Creditor,
)
from pyrtos.forms import (
    InvoiceCreateForm,
    InvoiceEditForm,
)

class InvoiceViews(object):

    def __init__(self,request):
        self.request = request

    @view_config(route_name='invoices',
                 renderer='pyrtos:templates/invoice/alist.mako',
                 permission='view')
    def invoices(self):
        result = {}
        private = self.request.params.get('private')
        if private:
            categories = Category.all_private(self.request).all()
        else:
            categories = Category.all_active().all()
        for c in categories:
            e = Invoice.with_category(c.id)
            if e:
              s = Invoice.with_category(c.id, total_only=True)
              result[c.title] = [e, s]
        return {'items': result,
                'title' : 'Private invoices' if private else 'Public invoices',
                'private' : private,}

    @view_config(route_name='invoices_archived',
                 renderer='pyrtos:templates/invoice/list.mako',
                 permission='view')
    def invoices_archived(self):
        page = int (self.request.params.get('page', 1))
        invoices = Invoice.page(self.request, page, archived=True)
        return {'paginator': invoices,
                'title' : 'Archived invoices',
                'archived' : True,}

    @view_config(route_name='invoice_new',
                 renderer='pyrtos:templates/invoice/edit.mako',
                 permission='create')
    def invoice_create(self):
        private = self.request.params.get('private')
        form = InvoiceCreateForm(self.request.POST, csrf_context=self.request.session)
        if private:
            if not Category.first_private(self.request):
                self.request.session.flash('You must create at least one private category\
                                            before you can create private invoices', 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            if not Creditor.first_private(self.request):
                self.request.session.flash('You must create at least one private creditor\
                                            before you can create private invoices', 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            form.category_id.query = Category.all_private(self.request)
            form.creditor_id.query = Creditor.all_private(self.request)
        else:
            if not Category.first_active():
                self.request.session.flash('You must create at least one category\
                                            before you can create invoices', 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            if not Creditor.first_active():
                self.request.session.flash('You must create at least one creditor\
                                            before you can create invoices', 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            form.category_id.query = Category.all_active()
            form.creditor_id.query = Creditor.all_active()
        if self.request.method == 'POST' and form.validate():
            e = Invoice()
            form.populate_obj(e)
            e.user_id = authenticated_userid(self.request)
            e.category_id = form.category_id.data.id
            e.creditor_id = form.creditor_id.data.id
            DBSession.add(e)
            self.request.session.flash('Invoice %s created' % (e.title), 'success')
            if private:
                return HTTPFound(location=self.request.route_url('invoices', _query={'private' : 1}))
            return HTTPFound(location=self.request.route_url('invoices'))
        return {'title': 'New private invoice' if private else 'New invoice',
                'form': form,
                'action': 'invoice_new',
                'private' : private}

    @view_config(route_name='invoice_edit',
                 renderer='pyrtos:templates/invoice/edit.mako',
                 permission='edit')
    def invoice_edit(self):
        id = int(self.request.matchdict.get('id'))
        e = Invoice.by_id(id)
        if not e:
            return HTTPNotFound()
        form = InvoiceEditForm(self.request.POST, e, csrf_context=self.request.session)
        private = self.request.params.get('private')
        if private:
            form.category_id.query = Category.all_private(self.request)
            form.creditor_id.query = Creditor.all_private(self.request)
        else:
            form.category_id.query = Category.all_active()
            form.creditor_id.query = Creditor.all_active()
        if self.request.method == 'POST' and form.validate():
            form.populate_obj(e)
            e.category_id = form.category_id.data.id
            e.creditor_id = form.creditor_id.data.id
            self.request.session.flash('Invoice %s updated' % (e.title), 'status')
            if private:
                return HTTPFound(location=self.request.route_url('invoices', _query={'private' : 1}))
            return HTTPFound(location=self.request.route_url('invoices'))
        form.category_id.data = e.category
        form.creditor_id.data = e.creditor
        return {'title' : 'Edit private invoice' if private else 'Edit invoice',
                'form' : form,
                'id' : id,
                'action' : 'invoice_edit',
                'private' : private}

    @view_config(route_name='invoice_archive',
                 renderer='string',
                 permission='archive')
    def invoice_archive(self):
        id = int(self.request.matchdict.get('id'))
        c = Invoice.by_id(id)
        if not c:
            return HTTPNotFound()
        c.archived = True
        DBSession.add(c)
        self.request.session.flash('Invoice %s archived' % (c.title), 'status')
        return HTTPFound(location=self.request.route_url('invoices'))

    @view_config(route_name='invoice_restore',
                 renderer='string',
                 permission='restore')
    def invoice_restore(self):
        id = int(self.request.matchdict.get('id'))
        c = Invoice.by_id(id)
        if not c:
            return HTTPNotFound()
        c.archived = False
        DBSession.add(c)
        self.request.session.flash('Invoice %s restored' % (c.title), 'status')
        return HTTPFound(location=self.request.route_url('invoices_archived'))

