<%inherit file="pyrtos:templates/base.mako"/>

<h1>${title}</h1>
<div class="upper_toolbar">
  %if action is not 'user_profile':
  <ul>
    %if request.can_i('create'):
      <li><a href="${request.route_url('user_new')}">New</a></li>
    %endif
    <li><a href="${request.route_url('users')}">All</a></li>
    %if request.can_i('archive'):
      <li><a href="${request.route_url('users_archived')}">Archived</a></li>
    %endif
  </ul>
  %endif
</div>

${next.body()} 
