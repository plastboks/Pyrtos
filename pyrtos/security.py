from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
)

class EntryFactory(object):
    __acl__ = [(Allow, Authenticated, 'view'),
               (Allow, Authenticated, 'create'),
               (Allow, Authenticated, 'edit'),
               (Allow, Authenticated, 'delete'),]

    def __init__(self, request):
        pass
