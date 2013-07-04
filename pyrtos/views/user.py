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

    def __init__(self,request):
        self.request = request

    @view_config(route_name='users',
                 renderer='pyrtos:templates/user/list.mako',
                 permission='view')
    def users(self):
        page = int (self.request.params.get('page', 1))
        users = User.page(self.request, page)
        return {'paginator': users,
                'title' : 'Users',}

    @view_config(route_name='user_new',
                 renderer='pyrtos:templates/user/edit.mako',
                 permission='create')
    def user_create(self):
        form = UserCreateForm(self.request.POST, csrf_context=self.request.session)
        if self.request.method == 'POST' and form.validate():
            u = User()
            form.populate_obj(u)
            DBSession.add(u)
            self.request.session.flash('User %s created' % (u.email), 'success')
            return HTTPFound(location=self.request.route_url('users'))
        return {'title': 'New user',
                'form': form,
                'action': 'user_new'}
