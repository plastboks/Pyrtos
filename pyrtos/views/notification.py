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
    WeekFilter,
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

        if self.request.method == 'POST' and form.validate():
            w = WeekFilter()
            for day in form.weekfilter.data:
                setattr(w, day, True)
            DBSession.add(w)
            n = Notification()
            del form.weekfilter
            form.populate_obj(n)
            n.user_id = authenticated_userid(self.request)
            n.weekfilter_id = w.id
            DBSession.add(n)
            self.request.session.flash('Notification %s created' %
                                       n.title,
                                       'success')
            return HTTPFound(location=self.request.route_url('notifications'))

        return {'title': 'New notification',
                'form': form,
                'action': 'notification_new'}

    @view_config(route_name='notification_edit',
                 renderer='pyrtos:templates/notification/edit.mako',
                 permission='edit')
    def notification_edit(self):
        """ Edit notification view. This method handles both post,
        and get requests. """

        uid = authenticated_userid(self.request)
        nid = int(self.request.matchdict.get('id'))
        n = Notification.by_id(uid, nid)

        if not n:
            return HTTPNotFound()

        form = NotificationEditForm(self.request.POST, n,
                                    csrf_context=self.request.session)
        active_days = []
        """ This is retarted, and should be improved """
        if n.weekfilter.monday:
            active_days.append('monday')
        if n.weekfilter.tuesday:
            active_days.append('tuesday')
        if n.weekfilter.wednesday:
            active_days.append('wednesday')
        if n.weekfilter.thursday:
            active_days.append('thursday')
        if n.weekfilter.friday:
            active_days.append('friday')
        if n.weekfilter.saturday:
            active_days.append('saturday')
        if n.weekfilter.sunday:
            active_days.append('sunday')

        if self.request.method == 'POST' and form.validate():
            """ Sigh... """
            w = WeekFilter.by_id(n.weekfilter.id)
            w.monday = False
            w.tuesday = False
            w.wednesday = False
            w.thursday = False
            w.friday = False
            w.saturday = False
            w.sunday = False
            for day in form.weekfilter.data:
                setattr(w, day, True)
            DBSession.add(w)
            del form.weekfilter
            form.populate_obj(n)
            self.request.session.flash('Notification %s updated' %
                                       (n.title), 'status')
            return HTTPFound(location=self.request.route_url('notifications'))

        form.weekfilter.data = active_days
        return {'title': 'Edit notification',
                'id': nid,
                'form': form,
                'action': 'notification_edit'}
