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
    Tag,
)


class TagViews(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='tags',
                 renderer='pyrtos:templates/tag/list.mako',
                 permission='view')
    def tags(self):
        """ Return list of tags. Unused for now. """

        tags = Tag.popular()
        return {'tags': tags,
                'title': 'Tags'}
