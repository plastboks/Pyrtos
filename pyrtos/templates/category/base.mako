<%inherit file="pyrtos:templates/base.mako"/>

<h1>${title}</h1>
<div class="upper_toolbar">
  <ul>
    <li><a href="${request.route_url('category_new')}">New</a></li>
    <li><a href="${request.route_url('categories')}">All</a></li>
    <li><a href="${request.route_url('categories_archived')}">Archived</a></li>
  </ul>
</div>

${next.body()} 
