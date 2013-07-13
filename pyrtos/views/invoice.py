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
    InvoiceSearchForm,
)

class InvoiceViews(object):

    missing_priv_cat = 'You must create at least one private category\
                       before you can create private invoices'
    missing_priv_cred = 'You must create at least one private creditor\
                         before you can create private invoices'
    missing_shared_cat = 'You must create at least one category\
                          before you can create invoices'
    missing_shared_cred = 'You must create at least one creditor\
                           before you can create invoices'

    def __init__(self,request):
        self.request = request

    
    def update_flash(self): 
        shared_unpaid_invoices = 0;
        shared_categories = Category.all_active(self.request).all()
        for c in shared_categories:
            unpaid_invoices = Invoice.with_category_all_unpaid(c.id)
            if unpaid_invoices:
                shared_unpaid_invoices += len(unpaid_invoices)
        self.request.session.pop_flash('shared_unpaid_invoices')
        self.request.session.flash(shared_unpaid_invoices,
                                   'shared_unpaid_invoices')

        private_unpaid_invoices = 0;
        private_categories = Category.all_private(self.request).all()
        for c in private_categories:
            unpaid_invoices = Invoice.with_category_all_unpaid(c.id)
            if unpaid_invoices:
                private_unpaid_invoices += len(unpaid_invoices)
        self.request.session.pop_flash('private_unpaid_invoices')
        self.request.session.flash(private_unpaid_invoices,
                                   'private_unpaid_invoices')


    def month_switcher(self, year, month, next=False):
        if next:
            if month >= 12:
                return [year+1, 1]
            return [year, month+1]
        if month <= 1:
            return [year-1, 12]
        return [year, month-1]


    @view_config(route_name='invoices',
                 renderer='pyrtos:templates/invoice/alist.mako',
                 permission='view')
    def invoices(self):
        paid_result = {}
        unpaid_result = {}
        year = int(self.request.params.get('year',
                                           datetime.now().strftime('%Y')))
        month = int(self.request.params.get('month',
                                            datetime.now().strftime('%m')))

        categories = Category.all_active(self.request).all()

        for c in categories:
            paid_invoices = Invoice.with_category_paid(c.id,
                                                       year,
                                                       month)
            if paid_invoices:
                total = Invoice.with_category_paid(c.id,
                                                   year,
                                                   month,
                                                   total_only=True)
                paid_result[c.title] = [paid_invoices, total]

            unpaid_invoices = Invoice.with_category_all_unpaid(c.id)
            if unpaid_invoices:
                total = Invoice.with_category_all_unpaid(c.id, total_only=True)
                unpaid_result[c.title] = [unpaid_invoices, total]

        return {'paiditems': paid_result,
                'unpaiditems' : unpaid_result,
                'title' : 'Invoices',
                'month' : month,
                'year' : year,
                'nextmonth' : self.month_switcher(year, month, next=True),
                'prevmonth' : self.month_switcher(year, month)}


    @view_config(route_name='invoices_search',
                 renderer='pyrtos:templates/invoice/list.mako',
                 permission='view')
    def invoices_search(self):
       page = int(self.request.params.get('page', 1)) 
       form = InvoiceSearchForm(self.request.POST,
                                csrf_context=self.request.session)
       form.categories.query = Category.all_active(self.request)
       form.creditors.query = Creditor.all_active(self.request)
       if self.request.method == 'POST' and form.validate():
           q = form.query.data
           categories = form.categories.data
           creditors = form.creditors.data
           invoices = Invoice.searchpage(self.request,
                                         page,
                                         qry=q,
                                         categories=categories,
                                         creditors=creditors)
           total = Invoice.searchpage(self.request,
                                         page,
                                         qry=q,
                                         categories=categories,
                                         creditors=creditors,
                                         total_only=True)
       else:
           invoices = Invoice.searchpage(self.request, page)
           total = Invoice.searchpage(self.request, page, total_only=True)
       return {'paginator': invoices,
               'form' : form,
               'title' : 'Search',
               'searchpage' : True,
               'total' : total}


    @view_config(route_name='invoices_archived',
                 renderer='pyrtos:templates/invoice/list.mako',
                 permission='view')
    def invoices_archived(self):
        page = int(self.request.params.get('page', 1))
        invoices = Invoice.page(self.request, page, archived=True)
        return {'paginator': invoices,
                'title' : 'Archived invoices',
                'searchpage' : False,
                'total' : False,}


    @view_config(route_name='invoice_new',
                 renderer='pyrtos:templates/invoice/edit.mako',
                 permission='create')
    def invoice_create(self):
        form = InvoiceCreateForm(self.request.POST,
                                 csrf_context=self.request.session)

        private = self.request.params.get('private')
        if private:
            if not Category.first_private(self.request):
                self.request.session.flash(self.missing_priv_cat)
                return HTTPFound(location=self.request.route_url('invoices'))
            if not Creditor.first_private(self.request):
                self.request.session.flash(self.missing_priv_cred)
                return HTTPFound(location=self.request.route_url('invoices'))
            form.category_id.query = Category.all_private(self.request)
            form.creditor_id.query = Creditor.all_private(self.request)
        else:
            if not Category.first_active():
                self.request.session.flash(self.missing_shared_cat, 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            if not Creditor.first_active():
                self.request.session.flash(self.missing_shared_cred, 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            form.category_id.query = Category.all_shared(self.request)
            form.creditor_id.query = Creditor.all_shared(self.request)

        if self.request.method == 'POST' and form.validate():
            i = Invoice()
            form.populate_obj(i)
            i.user_id = authenticated_userid(self.request)
            i.category_id = form.category_id.data.id
            i.creditor_id = form.creditor_id.data.id
            DBSession.add(i)
            self.request.session.flash('Invoice %s created' %\
                                          (i.title), 'success')
            self.update_flash()
            if private:
                return HTTPFound(location=self.request.route_url('invoices',
                                                                 _query={'private' : 1}))
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
        i = Invoice.by_id(id)

        if not i:
            return HTTPNotFound()
        if i.category.private\
            and i.category.user_id is not authenticated_userid(self.request):
            return HTTPForbidden()
        if i.creditor.private\
            and i.creditor.user_id is not authenticated_userid(self.request):
            return HTTPForbidden()

        form = InvoiceEditForm(self.request.POST, i, 
                               csrf_context=self.request.session)

        private = self.request.params.get('private')
        if private:
            if not Category.first_private(self.request):
                self.request.session.flash(self.missing_priv_cat, 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            if not Creditor.first_private(self.request):
                self.request.session.flash(self.missing_priv_cred, 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            form.category_id.query = Category.all_private(self.request)
            form.creditor_id.query = Creditor.all_private(self.request)
        else:
            if not Category.first_active():
                self.request.session.flash(self.missing_shared_cat, 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            if not Creditor.first_active():
                self.request.session.flash(self.missing_shared_cred, 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            form.category_id.query = Category.all_shared(self.request)
            form.creditor_id.query = Creditor.all_shared(self.request)

        if self.request.method == 'POST' and form.validate():
            form.populate_obj(i)
            i.category_id = form.category_id.data.id
            i.creditor_id = form.creditor_id.data.id
            self.request.session.flash('Invoice %s updated' %\
                                          (i.title), 'status')
            self.update_flash()
            if private:
                return HTTPFound(location=self.request.route_url('invoices', 
                                                                 _query={'private' : 1}))
            return HTTPFound(location=self.request.route_url('invoices'))

        form.category_id.data = i.category
        form.creditor_id.data = i.creditor
        return {'title' : 'Edit private invoice' if private else 'Edit invoice',
                'form' : form,
                'id' : id,
                'action' : 'invoice_edit',
                'private' : private}


    @view_config(route_name='invoice_quickpay',
                 renderer='string',
                 permission='edit')
    def invoice_quickpay(self):
        id = int(self.request.matchdict.get('id'))
        i = Invoice.by_id(id)

        if not i:
            return HTTPNotFound()
        if i.category.private\
            and i.category.user_id is not authenticated_userid(self.request):
            return HTTPForbidden()
        if i.creditor.private\
            and i.creditor.user_id is not authenticated_userid(self.request):
            return HTTPForbidden()

        i.paid = datetime.now()
        self.request.session.flash('Invoice %s is now paid' %\
                                        (i.title), 'success')
        self.update_flash()
        return HTTPFound(location=self.request.route_url('invoices'))


    @view_config(route_name='invoice_archive',
                 renderer='string',
                 permission='archive')
    def invoice_archive(self):
        id = int(self.request.matchdict.get('id'))
        i = Invoice.by_id(id)

        if not i:
            return HTTPNotFound()
        if i.category.private\
            and i.category.user_id is not authenticated_userid(self.request):
            return HTTPForbidden()
        if i.creditor.private\
            and i.creditor.user_id is not authenticated_userid(self.request):
            return HTTPForbidden()

        i.archived = True
        DBSession.add(i)
        self.request.session.flash('Invoice %s archived' % (i.title), 'status')
        return HTTPFound(location=self.request.route_url('invoices'))

  
    @view_config(route_name='invoice_restore',
                 renderer='string',
                 permission='restore')
    def invoice_restore(self):
        id = int(self.request.matchdict.get('id'))
        i = Invoice.by_id(id)

        if not i:
            return HTTPNotFound()
        if i.category.private\
            and i.category.user_id is not authenticated_userid(self.request):
            return HTTPForbidden()
        if i.creditor.private\
            and i.creditor.user_id is not authenticated_userid(self.request):
            return HTTPForbidden()

        i.archived = False
        DBSession.add(i)
        self.request.session.flash('Invoice %s restored' % (i.title), 'status')
        return HTTPFound(location=self.request.route_url('invoices_archived'))

