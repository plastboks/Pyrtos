<%inherit file="pyrtos:templates/notification/base.mako"/>

%if paginator.items:
  <div class='tablelist'>
    <table id='notifications'>
      <thead>
        <th>Title</th>
        <th>DiA</th>
        <th>Hour</th>
        <th>Minute</th>
        <th>Mon</th>
        <th>Tue</th>
        <th>Wed</th>
        <th>Thur</th>
        <th>Fri</th>
        <th>Sat</th>
        <th>Sun</th>
        <th>Action</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr>
            <td>${item.title}</td>
            <td>${item.days_in_advance}</td>
            <td>${"%02d" % item.hour}</td>
            <td>${"%02d" % item.minute}</td>
            <td class="notification day">
              <span class="${item.weekfilter.monday}"><span>
            </td>
            <td class="notification day">
              <span class="${item.weekfilter.tuesday}"><span>
            </td>
            <td class="notification day">
              <span class="${item.weekfilter.wednesday}"><span>
            </td>
            <td class="notification day">
              <span class="${item.weekfilter.thursday}"><span>
            </td>
            <td class="notification day">
              <span class="${item.weekfilter.friday}"><span>
            </td>
            <td class="notification day">
              <span class="${item.weekfilter.saturday}"><span>
            </td>
            <td class="notification day">
              <span class="${item.weekfilter.sunday}"><span>
            </td>
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
