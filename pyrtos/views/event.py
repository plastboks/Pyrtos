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
    Event,
)


class EventViews(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='events',
                 renderer='pyrtos:templates/event/list.mako',
                 permission='view')
    def events(self):
        """ Get a paginated list of active events. """

        page = int(self.request.params.get('page', 1))
        events = Event.page(self.request, page)
        return {'paginator': events,
                'title': 'Events',
                'archived': False,
                }

    @view_config(route_name='events_archived',
                 renderer='pyrtos:templates/event/list.mako',
                 permission='view')
    def events_archived(self):
        """ Get a paginated list of archived events. """

        page = int(self.request.params.get('page', 1))
        events = Event.page(self.request, page, archived=True)
        return {'paginator': events,
                'title': 'Archived events',
                'archived': True,
                }
