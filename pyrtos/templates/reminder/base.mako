<%inherit file="pyrtos:templates/base.mako"/>

<h1>${title}</h1>
<div class="upper_toolbar">
  <ul>
    <li><a href="${request.route_url('reminders')}">Active</a></li>
    <li><a href="${request.route_url('reminders_inactive')}">Inactive</a></li>
  </ul>
</div>

${next.body()} 
