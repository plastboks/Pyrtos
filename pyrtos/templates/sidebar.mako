<ul>
  <li><a href="${request.route_url('index')}">Dashboard</a></li>
  <li><a href="${request.route_url('incomes')}">Incomes</a></li>
  <li><a href="${request.route_url('expenditures')}">Expenditures</a></li>
  <li>
      <a href="${request.route_url('invoices')}">Invoices</a>
      %if request.session.peek_flash('shared_unpaid_invoices')[0]:
        <sup class='unpaids shared'>${request.session.peek_flash('shared_unpaid_invoices')[0]}</sup>
      %endif
      %if request.session.peek_flash('private_unpaid_invoices')[0]:
        <sup class='unpaids private'>${request.session.peek_flash('private_unpaid_invoices')[0]}</sup>
      %endif
  </li>
</ul>
<ul>
  <li class='group'><a href="${request.route_url('creditors')}">Creditors</a></li>
  <li class='group'><a href="${request.route_url('categories')}">Categories</a></li>
  <li class='group'><a href="${request.route_url('tags')}">Tags</a></li>
</ul>
<ul>
  <li class='user'><a href="${request.route_url('users')}">Users</a></li>
  <li class='user'><a href="${request.route_url('logout')}">Logout</a></li>
</ul>
