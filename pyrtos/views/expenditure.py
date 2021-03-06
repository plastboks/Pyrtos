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
    Expenditure,
)
from pyrtos.forms import (
    ExpenditureCreateForm,
    ExpenditureEditForm,
)


class ExpenditureViews(object):

    """ Some commonly used strings. """
    missing_priv_cat = 'You must create at least one private category\
                        before you can create private expenditures'
    missing_shared_cat = 'You must create at least one category\
                          before you can create expenditures'

    def __init__(self, request):
        self.request = request

    @view_config(route_name='expenditures',
                 renderer='pyrtos:templates/expenditure/alist.mako',
                 permission='view')
    def expenditures(self):
        """ Return a paginated list of active expenditures.
        Handles both private and shared expenditures. """

        result = {}

        private = self.request.params.get('private')
        if private:
            categories = Category.all_private(self.request).all()
        else:
            categories = Category.all_active(self.request).all()

        for c in categories:
            e = Expenditure.with_category(c.id)
            if e:
                s = Expenditure.with_category(c.id, total_only=True)
                result[c.title] = [e, s]
        return {'items': result,
                'title': 'Private expenditures' if private
                         else 'Shared expenditures',
                'private': private}

    @view_config(route_name='expenditures_archived',
                 renderer='pyrtos:templates/expenditure/list.mako',
                 permission='view')
    def expenditures_archived(self):
        """ Returns a paginated list of archived expenditures."""

        page = int(self.request.params.get('page', 1))
        expenditures = Expenditure.page(self.request, page, archived=True)
        return {'paginator': expenditures,
                'title': 'Archived expenditures',
                'archived': True}

    @view_config(route_name='expenditure_new',
                 renderer='pyrtos:templates/expenditure/edit.mako',
                 permission='create')
    def expenditure_create(self):
        """ New expenditure. Method for both post and get request. """

        form = ExpenditureCreateForm(self.request.POST,
                                     csrf_context=self.request.session)

        private = self.request.params.get('private')
        if private:
            """ Check if there exists any private categories. """
            if not Category.first_private(self.request):
                self.request.session.flash(self.missing_priv_cat, 'error')
                return HTTPFound(location=self.request
                                              .route_url('expenditures'))
            form.category_id.query = Category.all_private(self.request)
        else:
            """ Check if there exists any categories. """
            if not Category.first_active():
                self.request.session.flash(self.missing_shared_cat, 'error')
                return HTTPFound(location=self.request
                                              .route_url('expenditures'))
            form.category_id.query = Category.all_active(self.request)

        if self.request.method == 'POST' and form.validate():
            e = Expenditure()
            form.populate_obj(e)
            e.user_id = authenticated_userid(self.request)
            e.category_id = form.category_id.data.id
            DBSession.add(e)
            self.request.session.flash('Expenditure %s created' %
                                       (e.title), 'success')
            """ A bit ugly, but redirect the user based on private or not. """
            if private:
                return HTTPFound(location=
                                 self.request
                                     .route_url('expenditures',
                                                _query={'private': 1}))
            return HTTPFound(location=self.request.route_url('expenditures'))
        return {'title': 'New private expenditure' if private
                         else 'New expenditure',
                'form': form,
                'action': 'expenditure_new',
                'private': private}

    @view_config(route_name='expenditure_edit',
                 renderer='pyrtos:templates/expenditure/edit.mako',
                 permission='edit')
    def expenditure_edit(self):
        """ Edit expenditure. Method for both post and get request. """

        id = int(self.request.matchdict.get('id'))

        e = Expenditure.by_id(id)
        if not e:
            return HTTPNotFound()

        """ Authorization check. """
        if (e.category.private
           and e.category.user_id is not authenticated_userid(self.request)):
            return HTTPForbidden()

        form = ExpenditureEditForm(self.request.POST, e,
                                   csrf_context=self.request.session)

        private = self.request.params.get('private')
        if private:
            """ Check if there exists any categories. """
            if not Category.first_private(self.request):
                self.request.session.flash(self.missing_priv_cat, 'error')
                return HTTPFound(location=self.request
                                              .route_url('expenditures'))
            form.category_id.query = Category.all_private(self.request)
        else:
            """ Check if there exists any categories. """
            if not Category.first_active():
                self.request.session.flash(self.missing_shared_cat, 'error')
                return HTTPFound(location=self.request
                                              .route_url('expenditures'))
            form.category_id.query = Category.all_active(self.request)

        if self.request.method == 'POST' and form.validate():
            form.populate_obj(e)
            e.category_id = form.category_id.data.id
            self.request.session.flash('Expenditure %s updated' %
                                       (e.title), 'status')
            """ A bit ugly, but redirect the user based on private or not. """
            if private:
                return HTTPFound(location=
                                 self.request
                                     .route_url('expenditures',
                                                _query={'private': 1}))
            return HTTPFound(location=self.request.route_url('expenditures'))

        form.category_id.data = e.category
        return {'title': 'Edit private expenditure' if private
                         else 'Edit expenditure',
                'form': form,
                'id': id,
                'expenditure': e,
                'action': 'expenditure_edit',
                'private': private}

    @view_config(route_name='expenditure_archive',
                 renderer='string',
                 permission='archive')
    def expenditure_archive(self):
        """ Archive expenditure, returns redirect. """

        id = int(self.request.matchdict.get('id'))

        e = Expenditure.by_id(id)
        if not e:
            return HTTPNotFound()

        """ Authorization check. """
        if (e.category.private
           and e.category.user_id is not authenticated_userid(self.request)):
            return HTTPForbidden()

        e.archived = True
        DBSession.add(e)
        self.request.session.flash('Expenditure %s archived' %
                                   (e.title), 'status')
        return HTTPFound(location=self.request.route_url('expenditures'))

    @view_config(route_name='expenditure_restore',
                 renderer='string',
                 permission='restore')
    def expenditure_restore(self):
        """ Restore expenditure, return redirect. """

        id = int(self.request.matchdict.get('id'))

        e = Expenditure.by_id(id)
        if not e:
            return HTTPNotFound()

        """ Authorization check. """
        if (e.category.private
           and e.category.user_id is not authenticated_userid(self.request)):
            return HTTPForbidden()

        e.archived = False
        DBSession.add(e)
        self.request.session.flash('Expenditure %s restored' %
                                   (e.title), 'status')
        return HTTPFound(location=self.request
                                      .route_url('expenditures_archived'))
