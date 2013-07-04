<%inherit file="pyrtos:templates/base.mako"/>

<h1>${title}</h1>
<div class="upper_toolbar">
  <ul>
    <li><a href="${request.route_url('tags')}">All</a></li>
  </ul>
</div>

%if tags:
  %for tag in tags:
    <span>${tag}</span>
  %endfor
%else:
  <p>No tags found.</p>
%endif
