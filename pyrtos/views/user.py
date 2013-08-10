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
)
from pyrtos.models.meta import DBSession
from pyrtos.models import (
    User,
)
from pyrtos.forms import (
    UserCreateForm,
    UserEditForm,
)


class UserViews(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='users',
                 renderer='pyrtos:templates/user/list.mako',
                 permission='view')
    def users(self):
        """ Get a paginated list of active users. """

        page = int(self.request.params.get('page', 1))
        users = User.page(self.request, page)
        return {'paginator': users,
                'title': 'Users',
                'archived': False,
                'myid': authenticated_userid(self.request)}

    @view_config(route_name='users_archived',
                 renderer='pyrtos:templates/user/list.mako',
                 permission='view')
    def users_archived(self):
        """ Get a paginated list of archived users. """

        page = int(self.request.params.get('page', 1))
        users = User.page(self.request, page, archived=True)
        return {'paginator': users,
                'title': 'Archived users',
                'archived': True,
                'myid': authenticated_userid(self.request)}

    @view_config(route_name='user_new',
                 renderer='pyrtos:templates/user/edit.mako',
                 permission='create')
    def user_create(self):
        """ New user view. Method handles both post and get
        requests.
        """

        form = UserCreateForm(self.request.POST,
                              csrf_context=self.request.session)

        if self.request.method == 'POST' and form.validate():
            u = User()
            form.populate_obj(u)
            u.password = u.pm.encode(form.password.data)
            DBSession.add(u)
            self.request.session.flash('User %s created' %
                                       (u.email), 'success')
            return HTTPFound(location=self.request.route_url('users'))
        return {'title': 'New user',
                'form': form,
                'action': 'user_new'}

    @view_config(route_name='user_edit',
                 renderer='pyrtos:templates/user/edit.mako',
                 permission='edit')
    def user_edit(self):
        """ Edit user view. Method handles both post and get
        requests.
        """

        a = authenticated_userid(self.request)
        id = int(self.request.matchdict.get('id'))

        """ User one (1) is a bit special..."""
        if id is 1 and a is not 1:
            return HTTPNotFound()

        u = User.by_id(id)
        if not u:
            return HTTPNotFound()

        form = UserEditForm(self.request.POST, u,
                            csrf_context=self.request.session)

        if self.request.method == 'POST' and form.validate():
            form.populate_obj(u)
            if u.password:
                u.password = u.pm.encode(form.password.data)
            else:
                del u.password
            self.request.session.flash('User %s updated' %
                                       (u.email), 'status')
            return HTTPFound(location=self.request.route_url('users'))
        return {'title': 'Edit user',
                'form': form,
                'id': id,
                'myid': a,
                'user': u,
                'action': 'user_edit'}

    @view_config(route_name='user_archive',
                 renderer='string',
                 permission='archive')
    def user_archive(self):
        """ Archive user, returns redirect. """

        a = authenticated_userid(self.request)
        id = int(self.request.matchdict.get('id'))

        """ User one (1) is a bit special..."""
        if id is 1:
            return HTTPNotFound()

        u = User.by_id(id)
        if not u:
            return HTTPNotFound()

        u.archived = True
        DBSession.add(u)
        self.request.session.flash('User %s archived' %
                                   (u.email), 'status')
        return HTTPFound(location=self.request.route_url('users'))

    @view_config(route_name='user_restore',
                 renderer='string',
                 permission='restore')
    def user_restore(self):
        """ Restore user, returns redirect. """

        id = int(self.request.matchdict.get('id'))

        u = User.by_id(id)
        if not u:
            return HTTPNotFound()

        u.archived = False
        DBSession.add(u)
        self.request.session.flash('User %s restored' %
                                   (u.email), 'status')
        return HTTPFound(location=self.request.route_url('users_archived'))
