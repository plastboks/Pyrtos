<%inherit file="pyrtos:templates/base.mako"/>

<h1>${title}</h1>
<div class="upper_toolbar">
  <ul>
    %if request.can_i('create'):
      <li><a href="${request.route_url('income_new')}">New</a></li>
    %endif
    <li><a href="${request.route_url('incomes')}">All</a></li>
    %if request.can_i('archive'):
      <li><a href="${request.route_url('incomes_archived')}">Archived</a></li>
    %endif
  </ul>
</div>

${next.body()} 
