<%inherit file="pyrtos:templates/base.mako"/>

<h1>${title}</h1>
<div class="upper_toolbar">
  <ul>
    %if request.can_i('create'):
      <li><a href="${request.route_url('notification_new')}">New</a></li>
    %endif
    <li><a href="${request.route_url('notifications')}">All</a></li>
    <li><a href="${request.route_url('notifications_archived')}">Archived</a></li>
  </ul>
</div>

${next.body()}
