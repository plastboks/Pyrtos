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
    """
    A standard Pyramid EntryFactory object snagged and extended
    from one of the pyramid tutorials @ readthedocs.

    This is just a simple mockup class for the begining of the
    project.
    """
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
    """
    A simple groupfinder for picking the right permission
    to the right users.

    userid -- integer, userid.
    request -- object, standard request object.
    """
    user = User.by_id(userid)
    group = user.group
    return ['group:'+group]


def can_i(request, perm):
    """
    Function for checking permisssions based on users group
    identification. This function is made for use in templates.

    request -- object, standard request object.
    perm -- string, for matching against group permission.
    """
    return has_permission(perm, request.context, request)
