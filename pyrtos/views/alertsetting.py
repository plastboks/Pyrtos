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
    AlertSetting,
    WeekFilter,
)
from pyrtos.forms import (
    AlertSettingCreateForm,
    AlertSettingEditForm,
)


class AlertSettingViews(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='alertsettings',
                 renderer='pyrtos:templates/alertsetting/list.mako',
                 permission='view')
    def alertsettings(self):
        """ Return list of alertsettings."""

        page = int(self.request.params.get('page', 1))
        alertsettings = AlertSetting.page(self.request, page)
        return {'paginator': alertsettings,
                'title': 'My alert settings',
                'archived': False}

    @view_config(route_name='alertsettings_archived',
                 renderer='pyrtos:templates/alertsetting/list.mako',
                 permission='view')
    def alertsettings_archived(self):
        """ Return list of archived alertsettings."""

        page = int(self.request.params.get('page', 1))
        alertsettings = AlertSetting.page(self.request, page, archived=True)
        return {'paginator': alertsettings,
                'title': 'My archived alert settings',
                'archived': True}

    @view_config(route_name='alertsetting_new',
                 renderer='pyrtos:templates/alertsetting/edit.mako',
                 permission='create')
    def alertsetting_create(self):
        """ New alertsetting.
        This method handles both post and get requests.
        """

        form = AlertSettingCreateForm(self.request.POST,
                                      csrf_context=self.request.session)

        if self.request.method == 'POST' and form.validate():
            w = WeekFilter()
            for day in form.weekfilter.data:
                setattr(w, day, True)
            DBSession.add(w)
            a = AlertSetting()
            del form.weekfilter
            form.populate_obj(a)
            a.user_id = authenticated_userid(self.request)
            a.weekfilter_id = w.id
            DBSession.add(a)
            self.request.session.flash('Alert setting %s created' %
                                       a.title,
                                       'success')
            return HTTPFound(location=self.request.route_url('alertsettings'))

        return {'title': 'New alert setting',
                'form': form,
                'action': 'alertsetting_new'}

    @view_config(route_name='alertsetting_edit',
                 renderer='pyrtos:templates/alertsetting/edit.mako',
                 permission='edit')
    def alertsetting_edit(self):
        """ Edit alertsetting view. This method handles both post,
        and get requests. """

        uid = authenticated_userid(self.request)
        nid = int(self.request.matchdict.get('id'))
        a = AlertSetting.by_id(uid, nid)

        if not a:
            return HTTPNotFound()

        form = AlertSettingEditForm(self.request.POST, a,
                                    csrf_context=self.request.session)
        active_days = []
        """ This is retarted, and should be improved """
        if a.weekfilter.monday:
            active_days.append('monday')
        if a.weekfilter.tuesday:
            active_days.append('tuesday')
        if a.weekfilter.wednesday:
            active_days.append('wednesday')
        if a.weekfilter.thursday:
            active_days.append('thursday')
        if a.weekfilter.friday:
            active_days.append('friday')
        if a.weekfilter.saturday:
            active_days.append('saturday')
        if a.weekfilter.sunday:
            active_days.append('sunday')

        if self.request.method == 'POST' and form.validate():
            """ Sigh... """
            w = WeekFilter.by_id(a.weekfilter.id)
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
            form.populate_obj(a)
            self.request.session.flash('Alert setting %s updated' %
                                       (a.title), 'status')
            return HTTPFound(location=self.request.route_url('alertsettings'))

        form.weekfilter.data = active_days
        return {'title': 'Edit alert setting',
                'id': nid,
                'form': form,
                'alertsetting': a,
                'action': 'alertsetting_edit'}

    @view_config(route_name='alertsetting_archive',
                 renderer='string',
                 permission='archive')
    def alertsetting_archive(self):
        """ Archive alertsetting, returns redirect. """

        uid = authenticated_userid(self.request)
        nid = int(self.request.matchdict.get('id'))

        a = AlertSetting.by_id(uid, nid)
        if not a:
            return HTTPNotFound()

        a.archived = True
        DBSession.add(a)
        self.request.session.flash('Alert setting %s archived' %
                                   (a.title), 'status')
        return HTTPFound(location=self.request.route_url('alertsettings'))

    @view_config(route_name='alertsetting_restore',
                 renderer='string',
                 permission='restore')
    def alertsetting_restore(self):
        """ Restore alertsetting, returns redirect. """

        uid = authenticated_userid(self.request)
        nid = int(self.request.matchdict.get('id'))

        a = AlertSetting.by_id(uid, nid)
        if not a:
            return HTTPNotFound()

        a.archived = False
        DBSession.add(a)
        self.request.session.flash('Alert setting %s restored' %
                                   (a.title), 'status')
        return HTTPFound(location=self.request
                                      .route_url('alertsettings_archived'))
