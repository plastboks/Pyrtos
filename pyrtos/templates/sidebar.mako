<ul>
  <li><a href="${request.route_url('index')}">Dashboard</a></li>
  <li><a href="${request.route_url('incomes')}">Incomes</a></li>
  <li><a href="${request.route_url('expenditures')}">Expenditures</a></li>
  <li>
      <a href="${request.route_url('invoices')}">Invoices</a>
      %if 1 is 2:
      <sup class='unpaids shared'>3</sup>
      <sup class='unpaids private'>3</sup>
      %endif
  </li>
  <li><a href="${request.route_url('creditors')}">Creditors</a></li>
</ul>
<ul>
  <li><a href="${request.route_url('categories')}">Categories</a></li>
  <li><a href="${request.route_url('tags')}">Tags</a></li>
  <li><a href="${request.route_url('users')}">Users</a></li>
  <li><a href="${request.route_url('logout')}">Logout</a></li>
</ul>
