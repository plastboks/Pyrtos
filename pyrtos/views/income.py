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
from pyrtos.models.meta import DBSession
from pyrtos.models import (
    User,
    Income,
)
from pyrtos.forms import (
    IncomeCreateForm,
    IncomeEditForm,
)


class IncomeViews(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='incomes',
                 renderer='pyrtos:templates/income/list.mako',
                 permission='view')
    def incomes(self):
        """ Get a paginated list of active incomes. """

        page = int(self.request.params.get('page', 1))
        incomes = Income.page(self.request, page)
        amount_sum = Income.amount_sum()
        return {'paginator': incomes,
                'title': 'Monthly incomes',
                'amount_sum': amount_sum,
                'archived': False}

    @view_config(route_name='incomes_archived',
                 renderer='pyrtos:templates/income/list.mako',
                 permission='view')
    def incomes_archived(self):
        """ Get a paginated list of archived incomes. """

        page = int(self.request.params.get('page', 1))
        incomes = Income.page(self.request, page, archived=True)
        return {'paginator': incomes,
                'title': 'Archived incomes',
                'archived': True}

    @view_config(route_name='income_new',
                 renderer='pyrtos:templates/income/edit.mako',
                 permission='create')
    def income_create(self):
        """ New income. This method handles both post and get requests. """

        form = IncomeCreateForm(self.request.POST,
                                csrf_context=self.request.session)
        form.user_id.query = User.all_users()

        if self.request.method == 'POST' and form.validate():
            i = Income()
            form.populate_obj(i)
            i.user_id = form.user_id.data.id
            DBSession.add(i)
            self.request.session.flash('Income %s created' %
                                       (i.title), 'success')
            return HTTPFound(location=self.request.route_url('incomes'))
        return {'title': 'New income',
                'form': form,
                'action': 'income_new'}

    @view_config(route_name='income_edit',
                 renderer='pyrtos:templates/income/edit.mako',
                 permission='edit')
    def income_edit(self):
        """ Edit income. This method handles both post and get requests. """

        id = int(self.request.matchdict.get('id'))

        """ Every user can edit every income object.
        So no authorization needed. """
        i = Income.by_id(id)
        if not i:
            return HTTPNotFound()

        form = IncomeEditForm(self.request.POST, i,
                              csrf_context=self.request.session)
        form.user_id.query = User.all_users()

        if self.request.method == 'POST' and form.validate():
            form.populate_obj(i)
            i.user_id = form.user_id.data.id
            self.request.session.flash('Income %s updated' %
                                       (i.title), 'status')
            return HTTPFound(location=self.request.route_url('incomes'))
        form.user_id.data = i.user
        return {'title': 'Edit income',
                'form': form,
                'id': id,
                'income': i,
                'action': 'income_edit'}

    @view_config(route_name='income_archive',
                 renderer='string',
                 permission='archive')
    def income_archive(self):
        """ Archive income, returns redirect. """

        id = int(self.request.matchdict.get('id'))

        """ Every user can edit every income object.
        So no authorization needed. """
        c = Income.by_id(id)
        if not c:
            return HTTPNotFound()

        c.archived = True
        DBSession.add(c)
        self.request.session.flash('Income %s archived' %
                                   (c.title), 'status')
        return HTTPFound(location=self.request.route_url('incomes'))

    @view_config(route_name='income_restore',
                 renderer='string',
                 permission='restore')
    def income_restore(self):
        """ Restores income, returns redirect. """

        id = int(self.request.matchdict.get('id'))

        """ Every user can edit every income object.
        So no authorization needed. """
        c = Income.by_id(id)
        if not c:
            return HTTPNotFound()

        c.archived = False
        DBSession.add(c)
        self.request.session.flash('Income %s restored' %
                                   (c.title), 'status')
        return HTTPFound(location=self.request.route_url('incomes_archived'))
