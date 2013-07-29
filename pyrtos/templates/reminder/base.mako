<%inherit file="pyrtos:templates/base.mako"/>

<h1>${title}</h1>
<div class="upper_toolbar">
  <ul>
    <li><a href="${request.route_url('reminders')}">All</a></li>
  </ul>
</div>

${next.body()} 
