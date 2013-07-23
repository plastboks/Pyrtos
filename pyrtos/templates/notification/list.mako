<%inherit file="pyrtos:templates/notification/base.mako"/>

%if paginator.items:
  <div class='tablelist'>
    <table id='notifications'>
      <thead>
        <th>Weekday</th>
        <th>Hour</th>
        <th>Minute</th>
        <th>Action</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr>
            <td>${item.weekday}</td>
            <td>${item.hour}</td>
            <td>${item.minute}</td>
            <td></td>
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
