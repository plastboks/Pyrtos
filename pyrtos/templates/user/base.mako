<%inherit file="pyrtos:templates/base.mako"/>

<h1>${title}</h1>
<div class="upper_toolbar">
  <ul>
    <li><a href="${request.route_url('user_new')}">New</a></li>
    <li><a href="${request.route_url('users')}">All</a></li>
    <li><a href="${request.route_url('users_archived')}">Archived</a></li>
  </ul>
</div>

${next.body()} 
