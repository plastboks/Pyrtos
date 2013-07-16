from pyramid.threadlocal import get_current_request

from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
    authenticated_userid,
    has_permission,
)

from pyrtos.models import User


class EntryFactory(object):
    __name__ = None
    __parent__ = None
    __acl__ = [(Allow, Authenticated, 'view'),
               (Allow, Authenticated, 'create'),
               (Allow, Authenticated, 'edit'),
               (Allow, 'group:admin', 'delete'),
               (Allow, 'group:admin', 'archive'),
               (Allow, 'group:admin', 'restore'), ]

    def __init__(self, request):
        pass


def groupfinder(userid, request):
    user = User.by_id(userid)
    group = user.group
    return ['group:'+group]


def can_i(request, perm):
    return has_permission(perm, request.context, request)
