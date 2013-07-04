<%inherit file="pyrtos:templates/user/base.mako"/>

%if paginator.items:
  <div class='tablelist'>
    <table id='users'>
      <thead>
        <th>Username</th>
        <th>Name</th>
        <th>Email</th>
        <th>Actions</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr>
            <td>${item.username}</td>
            <td>${item.givenname} ${item.surname}</td>
            <td>${item.email}</td>
            <td></td>
          </tr>
        %endfor
      </tbody>
    </table>
  </div>
  ${paginator.pager()}
%else:
  <p>No users found.</p>
%endif
