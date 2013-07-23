<%inherit file="pyrtos:templates/notification/base.mako"/>

%if paginator.items:
  <div class='tablelist'>
    <table id='notifications'>
      <thead>
        <th>Title</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr>
            <td>${item.title}</td>
          </tr>
        %endfor
      </tbody>
    </table>
  </div>
  <div class='pager'>
    ${paginator.pager()}
  </div>
%else:
  <p>No notifications found.</p>
%endif
