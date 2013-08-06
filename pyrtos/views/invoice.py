import random
import string
import os
import hashlib
import shutil

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
    File,
    Reminder,
)
from pyrtos.forms import (
    InvoiceCreateForm,
    InvoiceEditForm,
    InvoiceSearchForm,
)


class InvoiceViews(object):

    """ Some commonly used strings. """
    missing_priv_cat = 'You must create at least one private category\
                       before you can create private invoices'
    missing_priv_cred = 'You must create at least one private creditor\
                         before you can create private invoices'
    missing_shared_cat = 'You must create at least one category\
                          before you can create invoices'
    missing_shared_cred = 'You must create at least one creditor\
                           before you can create invoices'

    def __init__(self, request):
        self.request = request

    def update_flash(self):
        """ Since so many methods in this class did the exact same thing,
        a function was created. This updated the session invoice counter,
        used in many places (eg. sidebar).
        """

        shared_unpaid_invoices = 0
        shared_categories = Category.all_active(self.request).all()
        for c in shared_categories:
            unpaid_invoices = Invoice.with_category_all_unpaid(c.id)
            if unpaid_invoices:
                shared_unpaid_invoices += len(unpaid_invoices)
        self.request.session.pop_flash('shared_unpaid_invoices')
        self.request.session.flash(shared_unpaid_invoices,
                                   'shared_unpaid_invoices')

        private_unpaid_invoices = 0
        private_categories = Category.all_private(self.request).all()
        for c in private_categories:
            unpaid_invoices = Invoice.with_category_all_unpaid(c.id)
            if unpaid_invoices:
                private_unpaid_invoices += len(unpaid_invoices)
        self.request.session.pop_flash('private_unpaid_invoices')
        self.request.session.flash(private_unpaid_invoices,
                                   'private_unpaid_invoices')

    def randomstr(self, length):
        """ Random string generator. This function was created for sprinkling
        the file titles created by the edit and create invoice methods.
        Returns a string with the specified length.

        length -- int, string length.
        """

        return ''.join(random.choice(string.lowercase) for i in range(length))

    def month_switcher(self, year, month, next=False):
        """ A simple method for getting the next month,
        based on input year and month. Returns a list with ['year', 'month'].

        year -- int, four digit year.
        month -- int, month.
        next -- boolean, used for determing forward or backward result.
        """

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
        """ Get a paginated list of active invoices for current
        or given month."""

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
                'unpaiditems': unpaid_result,
                'title': 'Invoices',
                'month': month,
                'year': year,
                'nextmonth': self.month_switcher(year, month, next=True),
                'prevmonth': self.month_switcher(year, month)}

    @view_config(route_name='invoices_search',
                 renderer='pyrtos:templates/invoice/list.mako',
                 permission='view')
    def invoices_search(self):
        """ Get a list of invoices based on search arguments. """

        page = int(self.request.params.get('page', 1))
        form = InvoiceSearchForm(self.request.GET,
                                 csrf_context=self.request.session)
        form.categories.query = Category.all_active(self.request)
        form.creditors.query = Creditor.all_active(self.request)
        if self.request.method == 'GET' and form.validate():
            q = form.query.data
            categories = form.categories.data
            creditors = form.creditors.data
            fromdate = form.fromdate.data
            todate = form.todate.data
            invoices = Invoice.searchpage(self.request,
                                          page,
                                          qry=q,
                                          categories=categories,
                                          creditors=creditors,
                                          fromdate=fromdate,
                                          todate=todate,
                                          )
            total = Invoice.searchpage(self.request,
                                       page,
                                       qry=q,
                                       categories=categories,
                                       creditors=creditors,
                                       fromdate=fromdate,
                                       todate=todate,
                                       total_only=True,
                                       )
        else:
            invoices = Invoice.searchpage(self.request, page)
            total = Invoice.searchpage(self.request, page, total_only=True)
        return {'paginator': invoices,
                'form': form,
                'title': 'Search',
                'searchpage': True,
                'total': total}

    @view_config(route_name='invoices_archived',
                 renderer='pyrtos:templates/invoice/list.mako',
                 permission='view')
    def invoices_archived(self):
        """ Get a paginated list of archived invoices. """

        page = int(self.request.params.get('page', 1))
        invoices = Invoice.page(self.request, page, archived=True)
        return {'paginator': invoices,
                'title': 'Archived invoices',
                'searchpage': False,
                'total': False}

    @view_config(route_name='invoice_new',
                 renderer='pyrtos:templates/invoice/edit.mako',
                 permission='create')
    def invoice_create(self):
        """ New invoice view. This method handles both post,
        and get requests.
        """

        form = InvoiceCreateForm(self.request.POST,
                                 csrf_context=self.request.session)

        private = self.request.params.get('private')
        if private:
            """ Check if the necessary object exists. """
            if not Category.first_private(self.request):
                self.request.session.flash(self.missing_priv_cat)
                return HTTPFound(location=self.request.route_url('invoices'))
            if not Creditor.first_private(self.request):
                self.request.session.flash(self.missing_priv_cred)
                return HTTPFound(location=self.request.route_url('invoices'))
            form.category_id.query = Category.all_private(self.request)
            form.creditor_id.query = Creditor.all_private(self.request)
        else:
            """ Check if the necessary object exists. """
            if not Category.first_active():
                self.request.session.flash(self.missing_shared_cat, 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            if not Creditor.first_active():
                self.request.session.flash(self.missing_shared_cred, 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            form.category_id.query = Category.all_shared()
            form.creditor_id.query = Creditor.all_shared()

        if self.request.method == 'POST' and form.validate():
            i = Invoice()
            form.populate_obj(i)
            i.user_id = authenticated_userid(self.request)
            i.category_id = form.category_id.data.id
            i.creditor_id = form.creditor_id.data.id

            """ If file, make file object and save/create file. """
            upload = self.request.POST.get('attachment')
            try:
                f = File()
                f.filename = f.make_filename(upload.filename)
                f.filemime = f.guess_mime(upload.filename)
                f.write_file(upload.file)
                f.title = 'Invoice.' +\
                          form.title.data + '.' +\
                          self.randomstr(6) + '.' +\
                          form.category_id.data.title + '.' +\
                          form.creditor_id.data.title + '.' +\
                          str(i.due)
                if private:
                    f.private = True
                f.user_id = authenticated_userid(self.request)
                DBSession.add(f)
                i.files = [f]
            except Exception:
                self.request.session.flash('No file added.',
                                           'status')
            if form.reminder_true.data:
                r = Reminder()
                r.type = 1
                r.alert = form.due.data
                DBSession.add(r)
                DBSession.flush()
                i.reminder_id = r.id

            DBSession.add(i)
            self.request.session.flash('Invoice %s created' %
                                       (i.title), 'success')
            self.update_flash()
            if private:
                return HTTPFound(location=
                                 self.request
                                     .route_url('invoices',
                                                _query={'private': 1}))
            return HTTPFound(location=self.request.route_url('invoices'))
        return {'title': 'New private invoice' if private else 'New invoice',
                'form': form,
                'action': 'invoice_new',
                'private': private,
                'invoice': False}

    @view_config(route_name='invoice_edit',
                 renderer='pyrtos:templates/invoice/edit.mako',
                 permission='edit')
    def invoice_edit(self):
        """ Edit invoice view. This method handles both post,
        and get requests. """

        id = int(self.request.matchdict.get('id'))
        i = Invoice.by_id(id)

        if not i:
            return HTTPNotFound()
        """ Authorization check. """
        if (i.category.private
           and i.category.user_id is not authenticated_userid(self.request)):
            return HTTPForbidden()
        """ Authorization check. """
        if (i.creditor.private
           and i.creditor.user_id is not authenticated_userid(self.request)):
            return HTTPForbidden()

        form = InvoiceEditForm(self.request.POST, i,
                               csrf_context=self.request.session)

        if not i.files:
            del form.files
        else:
            form.files.query = i.files

        private = self.request.params.get('private')
        if private:
            """ Check if the necessary object exists. """
            if not Category.first_private(self.request):
                self.request.session.flash(self.missing_priv_cat, 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            if not Creditor.first_private(self.request):
                self.request.session.flash(self.missing_priv_cred, 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            form.category_id.query = Category.all_private(self.request)
            form.creditor_id.query = Creditor.all_private(self.request)
        else:
            """ Check if the necessary object exists. """
            if not Category.first_active():
                self.request.session.flash(self.missing_shared_cat, 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            if not Creditor.first_active():
                self.request.session.flash(self.missing_shared_cred, 'error')
                return HTTPFound(location=self.request.route_url('invoices'))
            form.category_id.query = Category.all_shared()
            form.creditor_id.query = Creditor.all_shared()

        if self.request.method == 'POST' and form.validate():
            form.populate_obj(i)
            i.category_id = form.category_id.data.id
            i.creditor_id = form.creditor_id.data.id

            if form.files:
                i.files = form.files.data

            """ If file, make file object and save/create file. """
            upload = self.request.POST.get('attachment')
            try:
                f = File()
                f.filename = f.make_filename(upload.filename)
                f.filemime = f.guess_mime(upload.filename)
                f.write_file(upload.file)
                f.title = 'Invoice.' +\
                          form.title.data + '.' +\
                          self.randomstr(6) + '.' +\
                          form.category_id.data.title + '.' +\
                          form.creditor_id.data.title + '.' +\
                          str(i.due)
                if private:
                    f.private = True
                f.user_id = authenticated_userid(self.request)
                DBSession.add(f)
                i.files.append(f)
            except Exception:
                self.request.session.flash('No file added.',
                                           'status')

            if form.reminder_true.data and i.reminder_id:
                i.reminder.alert = form.due.data
                i.reminder.active = True
            if form.reminder_true.data and not i.reminder_id:
                r = Reminder()
                r.type = 0
                r.alert = form.due.data
                DBSession.add(r)
                DBSession.flush()
                i.reminder_id = r.id
            if not form.reminder_true.data and i.reminder_id:
                i.reminder.active = False
            if form.paid.data and i.reminder_id:
                i.reminder.active = False
            else:
                i.reminder.active = True

            self.request.session.flash('Invoice %s updated' %
                                       (i.title), 'status')
            self.update_flash()
            if private:
                return HTTPFound(location=
                                 self.request
                                     .route_url('invoices',
                                                _query={'private': 1}))
            return HTTPFound(location=self.request.route_url('invoices'))

        form.category_id.data = i.category
        form.creditor_id.data = i.creditor
        if i.reminder_id and i.reminder.active:
            form.reminder_true.data = True
        return {'title': 'Edit private invoice' if private else 'Edit invoice',
                'form': form,
                'id': id,
                'action': 'invoice_edit',
                'private': private,
                'invoice': i}

    @view_config(route_name='invoice_quickpay',
                 renderer='string',
                 permission='edit')
    def invoice_quickpay(self):
        """ Quickpay method for making the 'just pay this invoice',
        often used function easier. """

        id = int(self.request.matchdict.get('id'))
        i = Invoice.by_id(id)

        if not i:
            return HTTPNotFound()
        """ Authorization check. """
        if (i.category.private
           and i.category.user_id is not authenticated_userid(self.request)):
            return HTTPForbidden()
        """ Authorization check. """
        if (i.creditor.private
           and i.creditor.user_id is not authenticated_userid(self.request)):
            return HTTPForbidden()

        i.paid = datetime.now()
        if i.reminder_id:
            i.reminder.active = False

        self.request.session.flash('Invoice %s is now paid' %
                                   (i.title), 'success')
        self.update_flash()
        return HTTPFound(location=self.request.route_url('invoices'))

    @view_config(route_name='invoice_archive',
                 renderer='string',
                 permission='archive')
    def invoice_archive(self):
        """ Archive invoice, returns redirect. """

        id = int(self.request.matchdict.get('id'))
        i = Invoice.by_id(id)

        if not i:
            return HTTPNotFound()
        """ Authorization check. """
        if (i.category.private
           and i.category.user_id is not authenticated_userid(self.request)):
            return HTTPForbidden()
        """ Authorization check. """
        if (i.creditor.private
           and i.creditor.user_id is not authenticated_userid(self.request)):
            return HTTPForbidden()

        i.archived = True
        DBSession.add(i)
        self.request.session.flash('Invoice %s archived' % (i.title), 'status')
        return HTTPFound(location=self.request.route_url('invoices'))

    @view_config(route_name='invoice_restore',
                 renderer='string',
                 permission='restore')
    def invoice_restore(self):
        """ Restore invoice, returns redirect. """
        id = int(self.request.matchdict.get('id'))
        i = Invoice.by_id(id)

        if not i:
            return HTTPNotFound()
        """ Authorization check. """
        if (i.category.private
           and i.category.user_id is not authenticated_userid(self.request)):
            return HTTPForbidden()
        """ Authorization check. """
        if (i.creditor.private
           and i.creditor.user_id is not authenticated_userid(self.request)):
            return HTTPForbidden()

        i.archived = False
        DBSession.add(i)
        self.request.session.flash('Invoice %s restored' % (i.title), 'status')
        return HTTPFound(location=self.request.route_url('invoices_archived'))
