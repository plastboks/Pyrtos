<%inherit file="pyrtos:templates/base.mako"/>

<h1>${title}</h1>
<div class="upper_toolbar">
  <ul>
    %if request.can_i('create'):
      <li><a href="${request.route_url('invoice_new')}">New</a></li>
    %endif
    <li><a href="${request.route_url('invoices')}">All</a></li>
    <li><a href="${request.route_url('invoices', _query={'private' : 1})}">Private</a></li>
    %if request.can_i('archive'):
      <li><a href="${request.route_url('invoices_archived')}">Archived</a></li>
    %endif
  </ul>
</div>

${next.body()} 
