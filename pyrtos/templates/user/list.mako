<%inherit file="pyrtos:templates/user/base.mako"/>

%if paginator.items:
  <div class='tablelist'>
    <table id='users'>
      <thead>
        <th>Name</th>
        <th>Email</th>
        <th>Actions</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr>
            <td>
            %if item.givenname:
              ${item.givenname}
            %endif
            %if item.surname:
              ${item.surname}</td>
            %endif
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
