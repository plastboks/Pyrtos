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
    Reminder,
)
from pyrtos.forms import (
    EventCreateForm,
    EventEditForm,
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

    @view_config(route_name='event_new',
                 renderer='pyrtos:templates/event/edit.mako',
                 permission='create')
    def event_create(self):
        """ New events. Method for both post and get request."""

        form = EventCreateForm(self.request.POST,
                               csrf_context=self.request.session)

        if self.request.method == 'POST' and form.validate():
            e = Event()
            e.user_id = authenticated_userid(self.request)
            form.populate_obj(e)
            if form.reminder_true.data:
                r = Reminder()
                r.type = 0
                r.alert = form.reminder_alert.data
                DBSession.add(r)
                DBSession.flush()
                e.reminder_id = r.id
            DBSession.add(e)
            self.request.session.flash('Event %s created' %
                                       (e.title), 'success')
            return HTTPFound(location=self.request.route_url('events'))
        return {'title': 'New event',
                'form': form,
                'action': 'event_new'}

    @view_config(route_name='event_edit',
                 renderer='pyrtos:templates/event/edit.mako',
                 permission='edit')
    def event_edit(self):
        """ Edit event. """

        id = int(self.request.matchdict.get('id'))

        e = Event.by_id(id)
        if not e:
            return HTTPNotFound()
        """ Authorization check. """
        if e.private and e.user_id is not authenticated_userid(self.request):
            return HTTPForbidden()

        form = EventEditForm(self.request.POST,
                             e,
                             csrf_context=self.request.session,
                             )

        if self.request.method == 'POST' and form.validate():
            form.populate_obj(e)
            if form.reminder_true.data and e.reminder_id:
                r = Reminder.by_id(e.reminder.id)
                r.alert = form.reminder_alert.data
                DBSession.add(r)
                self.request.session.flash('Event %s updated and\
                                            reminder updated' %
                                           (e.title), 'status')
            if form.reminder_true.data and not e.reminder_id:
                r = Reminder()
                r.type = 0
                r.alert = form.reminder_alert.data
                DBSession.add(r)
                DBSession.flush()
                e.reminder_id = r.id
                self.request.session.flash('Event %s updated and\
                                            reminder created' %
                                           (e.title), 'status')
            if not form.reminder_true.data and e.reminder_id:
                r = Reminder.by_id(e.reminder.id)
                DBSession.delete(r)
                self.request.session.flash('Event %s updated and\
                                            reminder deleted' %
                                           (e.title), 'status')
            return HTTPFound(location=self.request.route_url('events'))

        if e.reminder_id:
            r = Reminder.by_id(e.reminder.id)
            form.reminder_true.data = True
            form.reminder_alert.data = r.alert
        return {'title': 'Edit event',
                'form': form,
                'id': id,
                'action': 'event_edit'}

    @view_config(route_name='event_archive',
                 renderer='string',
                 permission='archive')
    def event_archive(self):
        """ Archive events, returns redirect. """

        id = int(self.request.matchdict.get('id'))

        e = Event.by_id(id)
        if not e:
            return HTTPNotFound()
        """ Authorization check. """
        if e.private and e.user_id is not authenticated_userid(self.request):
            return HTTPForbidden()

        e.archived = True
        DBSession.add(e)
        self.request.session.flash('Event %s archived' %
                                   (e.title), 'status')
        return HTTPFound(location=self.request.route_url('events'))

    @view_config(route_name='event_restore',
                 renderer='string',
                 permission='restore')
    def event_restore(self):
        """ Restore event, returns redirect. """

        id = int(self.request.matchdict.get('id'))

        e = Event.by_id(id)
        if not e:
            return HTTPNotFound()
        """ Authorization check. """
        if e.private and e.user_id is not authenticated_userid(self.request):
            return HTTPForbidden()

        e.archived = False
        DBSession.add(e)
        self.request.session.flash('Event %s restored' %
                                   (e.title), 'status')
        return HTTPFound(location=self.request.route_url('events_archived'))
