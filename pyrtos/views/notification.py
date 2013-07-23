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
    Notification,
)


class NotificationViews(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='notifications',
                 renderer='pyrtos:templates/notification/list.mako',
                 permission='view')
    def notifications(self):
        """ Return list of notificatoins."""

        page = int(self.request.params.get('page', 1))
        notifications = Notification.page(self.request, page)
        return {'paginator': notifications,
                'title': 'My notifications'}
