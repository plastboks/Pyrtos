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
from pyrtos.forms import (
    NotificationCreateForm,
    NotificationEditForm,
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

    @view_config(route_name='notification_new',
                 renderer='pyrtos:templates/notification/edit.mako',
                 permission='create')
    def notification_create(self):
        """ New notification.
        This method handles both post and get requests.
        """

        form = NotificationCreateForm(self.request.POST,
                                      csrf_context=self.request.session)

        """
        if self.request.method == 'POST' and form.validate():
            n = Notification()
            form.populate_obj(n)
            n.user_id = authenticated_userid(self.request)
            DBSession.add(n)
            self.request.session.flash('Notification %s created',
                                       'success')
            return HTTPFound(location=self.request.route_url('notifications'))
        """
        return {'title': 'New notification',
                'form': form,
                'action': 'notification_new'}
