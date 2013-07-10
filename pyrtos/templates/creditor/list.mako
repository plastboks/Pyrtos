<%inherit file="pyrtos:templates/creditor/base.mako"/>

%if paginator.items:
  <div class='tablelist'>
    <table id='creditors'>
      <thead>
        <th>Title</th>
        <th>Expenditures</th>
        <th>Actions</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr>
            <td>${item.title}</td>
            <td>${len(item.invoices)}</td>
            <td class='actions'>
              %if request.can_i('edit'):
                <a href="${request.route_url('creditor_edit', id=item.id)}">
                  <img src='${request.static_url("pyrtos:static/icons/page_white_edit.png")}' title='Edit' alt='Edit' />
                </a>
              %endif
              %if archived:
                %if request.can_i('restore'):
                  <a href="${request.route_url('creditor_restore', id=item.id)}">
                    <img src='${request.static_url("pyrtos:static/icons/page_white_restore.png")}' title='Restore' alt='Restore' />
                  </a>
                %endif
              %else:
                %if request.can_i('archive'):
                  <a href="${request.route_url('creditor_archive', id=item.id)}">
                    <img src='${request.static_url("pyrtos:static/icons/page_white_delete.png")}' title='Delete' alt='Delete' />
                  </a>
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
  <p>No creditors found.</p>
%endif
