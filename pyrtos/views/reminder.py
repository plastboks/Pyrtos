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
    Reminder,
)


class ReminderViews(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='reminders',
                 renderer='pyrtos:templates/reminder/list.mako',
                 permission='view')
    def reminders(self):
        """ Get a paginated list of active reminders. """

        page = int(self.request.params.get('page', 1))
        reminders = Reminder.page(self.request, page)
        return {'paginator': reminders,
                'title': 'Reminders',
                }
