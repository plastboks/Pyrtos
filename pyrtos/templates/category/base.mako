<%inherit file="pyrtos:templates/base.mako"/>

<h1>${title}</h1>
<div class="upper_toolbar">
  <ul>
    %if request.can_i('create'):
      <li><a href="${request.route_url('category_new')}">New</a></li>
    %endif
    <li><a href="${request.route_url('categories')}">All</a></li>
    %if request.can_i('archive'):
      <li><a href="${request.route_url('categories_archived')}">Archived</a></li>
    %endif
  </ul>
</div>

${next.body()} 
