from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    )


@view_config(route_name='index',
             renderer='pyrtos:templates/index.mako')
def index_page(request):
  return {'title': 'Hello world'}
