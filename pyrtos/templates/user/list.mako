<%inherit file="pyrtos:templates/user/base.mako"/>
%if paginator.items:
  <div class='tablelist'>
    <table id='users'>
      <thead>
        <th>Name</th>
        <th>Email</th>
        <th>Group</th>
        <th>Actions</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          %if item.blocked:
            <tr class='inactive'>
          %else:
            <tr class='active'>
          %endif

            <td>
            %if item.givenname:
              ${item.givenname}
            %endif
            %if item.surname:
              ${item.surname}</td>
            %endif
            <td>${item.email}</td>
            <td>${item.group}</td>
            <td class='actions'>
              %if item.id is not myid and item.id is not 1:
                %if request.can_i('edit'):
                  <a href="${request.route_url('user_edit', id=item.id)}">
                    <img src='${request.static_url("pyrtos:static/icons/page_white_edit.png")}' title='Edit' alt='Edit' />
                  </a>
                %endif
              %elif myid is item.id:
                <a href="${request.route_url('user_edit', id=item.id)}">
                  <img src='${request.static_url("pyrtos:static/icons/page_white_profile.png")}' title='Profile' alt='Profile' />
                </a>
              %endif

              %if item.id is not 1 and item.id is not myid: 
                %if archived:
                  %if request.can_i('restore'):
                    <a href="${request.route_url('user_restore', id=item.id)}">
                      <img src='${request.static_url("pyrtos:static/icons/page_white_restore.png")}' title='Restore' alt='Restore' />
                    </a>
                  %endif
                %else:
                  %if request.can_i('archive'):
                    <a href="${request.route_url('user_archive', id=item.id)}">
                      <img src='${request.static_url("pyrtos:static/icons/page_white_delete.png")}' title='Delete' alt='Delete' />
                    </a>
                  %endif
                %endif
              %endif
            </td>
          </tr>
        %endfor
      </tbody>
    </table>
  </div>
  <div class='pager'>
    ${paginator.pager()}
  </div>
%else:
  <p>No users found.</p>
%endif
