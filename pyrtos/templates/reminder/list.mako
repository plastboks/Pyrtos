<%inherit file="pyrtos:templates/reminder/base.mako"/>

%if paginator.items:
  <div class='tablelist'>
    <table id='reminders'>
      <thead>
        <th>ID</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr>
            <td>${item.id}</td>
          </tr>
        %endfor
      </tbody>
    </table>
  </div>
  <div class='pager'>
    ${paginator.pager()}
  </div>
%else:
  <p>No reminders found.</p>
%endif
