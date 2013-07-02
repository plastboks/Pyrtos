from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
)

class EntryFactory(object):
    __name__ = None
    __parent__ = None
    __acl__ = [(Allow, Authenticated, 'view'),
               (Allow, Authenticated, 'create'),
               (Allow, Authenticated, 'edit'),
               (Allow, Authenticated, 'delete'),]

    def __init__(self, request):
        pass
