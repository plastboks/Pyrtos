<%inherit file="pyrtos:templates/creditor/base.mako"/>

%if paginator.items:
  <div class='tablelist'>
    <table id='creditors'>
      <thead>
        <th>Title</th>
        <th>Name</th>
        <th>Actions</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr>
            <td>${item.title}</td>
            <td>${item.name}</td>
            <td class='actions'>
              %if request.can_i('edit'):
                <a href="${request.route_url('creditor_edit', id=item.id)}">Edit</a>
              %endif
              %if archived:
                %if request.can_i('restore'):
                  <a href="${request.route_url('creditor_restore', id=item.id)}">Restore</a>
                %endif
              %else:
                %if request.can_i('archive'):
                  <a href="${request.route_url('creditor_archive', id=item.id)}">Archive</a>
                %endif
              %endif
            </td>
          </tr>
        %endfor
      </tbody>
    </table>
  </div>
  ${paginator.pager()}
%else:
  <p>No creditors found.</p>
%endif
