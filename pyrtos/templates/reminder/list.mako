<%inherit file="pyrtos:templates/reminder/base.mako"/>

%if paginator.items:
  <section class='tablelist'>
    <table id='reminders'>
      <thead>
        <th>Type</th>
        <th>Alert</th>
        <th>Object</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr>
            <td>${item.types[item.type]}</td>
            <td>${item.alert.date()}</td>
            <td>
            %if item.event:
              Event: ${item.event[0].title}
            %endif
            %if item.invoice:
              Invoice: ${item.invoice[0].title}
            %endif
            </td>
          </tr>
        %endfor
      </tbody>
    </table>
  </section>
  <section class='pager'>
    ${paginator.pager()}
  </section>
%else:
  <p>No reminders found.</p>
%endif
