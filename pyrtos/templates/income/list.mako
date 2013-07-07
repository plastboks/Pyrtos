<%inherit file="pyrtos:templates/income/base.mako"/>

%if paginator.items:
  <div class='tablelist'>
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
                <a href="${request.route_url('income_edit', id=item.id)}">Edit</a>
              %endif
              %if archived:
                %if request.can_i('restore'):
                  <a href="${request.route_url('income_restore', id=item.id)}">Restore</a>
                %endif
              %else:
                %if request.can_i('archive'):
                  <a href="${request.route_url('income_archive', id=item.id)}">Archive</a>
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
  <p>No incomes found.</p>
%endif
