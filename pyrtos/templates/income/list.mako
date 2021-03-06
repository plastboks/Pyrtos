<%inherit file="pyrtos:templates/income/base.mako"/>

%if paginator.items:
  <section class='tablelist'>
    <table id='incomes'>
      <thead>
        <th>Title</th>
        <th>Amount</th>
        <th>User</th>
        <th>Actions</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr>
            <td>${item.title}</td>
            <td>${item.amount}</td>
            <td>${item.user.email}</td>
            <td class='actions'>
              %if request.can_i('edit'):
                <a href="${request.route_url('income_edit', id=item.id)}">
                    <img src='${request.static_url("pyrtos:static/icons/page_white_edit.png")}' title='Edit' alt='Edit' />
                </a>
              %endif
              %if archived:
                %if request.can_i('restore'):
                  <a href="${request.route_url('income_restore', id=item.id)}">
                    <img src='${request.static_url("pyrtos:static/icons/page_white_restore.png")}' title='Restore' alt='Restore' />
                  </a>
                %endif
              %else:
                %if request.can_i('archive'):
                  <a href="${request.route_url('income_archive', id=item.id)}">
                    <img src='${request.static_url("pyrtos:static/icons/page_white_delete.png")}' title='Delete' alt='Delete' />
                 </a>
                %endif
              %endif
            </td>
          </tr>
        %endfor
          %if amount_sum:
            <tr class='totalrow'>
              <td></td>
              <td colspan='3'>${amount_sum[0]}</td>
            </tr>
          %endif
      </tbody>
    </table>
  </section>
  <section class='pager'>
    ${paginator.pager()}
  </section>
%else:
  <p>No incomes found.</p>
%endif
