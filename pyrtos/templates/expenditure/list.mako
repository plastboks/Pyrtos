<%inherit file="pyrtos:templates/expenditure/base.mako"/>

%if paginator.items:
  <div class='tablelist'>
    <table id='expenditures'>
      <thead>
        <th>Title</th>
        <th>Amount</th>
        <th>Category</th>
        <th>Actions</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr>
            <td>${item.title}</td>
            <td>${item.amount}</td>
            <td>${item.category.title}</td>
            <td class='actions'>
              %if request.can_i('edit'):
                <a href="${request.route_url('expenditure_edit', id=item.id)}">
                    <img src='${request.static_url("pyrtos:static/icons/page_white_edit.png")}' title='Edit' alt='Edit' />
                </a>
              %endif
              %if archived:
                %if request.can_i('restore'):
                  <a href="${request.route_url('expenditure_restore', id=item.id)}">
                    <img src='${request.static_url("pyrtos:static/icons/page_white_restore.png")}' title='Restore' alt='Restore' />
                  </a>
                %endif
              %else:
                %if request.can_i('archive'):
                  <a href="${request.route_url('expenditure_archive', id=item.id)}">
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
  <div class='tablesum'>
  %if amount_sum:
    %for s in amount_sum:
      <span>Sum: ${s}</span>
    %endfor
  %endif
  </div>
  <div class='pager'>
    ${paginator.pager()}
  </div>
%else:
  <p>No expenditures found.</p>
%endif
