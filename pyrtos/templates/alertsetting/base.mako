<%inherit file="pyrtos:templates/base.mako"/>

<h1>${title}</h1>
<div class="upper_toolbar">
  <ul>
    %if request.can_i('create'):
      <li><a href="${request.route_url('alertsetting_new')}">New</a></li>
    %endif
    <li><a href="${request.route_url('alertsettings')}">All</a></li>
    <li><a href="${request.route_url('alertsettings_archived')}">Archived</a></li>
  </ul>
</div>

${next.body()}
