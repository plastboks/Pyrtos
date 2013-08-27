<%inherit file="pyrtos:templates/event/base.mako" />
<form action="${request.route_url(action, id=id)}" method="POST">
  ${form.csrf_token}
  %if action == 'event_edit':
    ${form.id()}
  %endif

  %for error in form.title.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.title.label}<br />
    ${form.title}
  </p>

  %for error in form.from_date.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.from_date.label}<br />
    ${form.from_date}
  </p>

  %for error in form.to_date.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.to_date.label}<br />
    ${form.to_date}
  </p>

  %for error in form.reminder_true.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.reminder_true.label}
    ${form.reminder_true}
  </p>

  %for error in form.reminder_alert.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.reminder_alert.label}
    ${form.reminder_alert}
  </p>

  <p>
    ${form.private.label}
    ${form.private}
  </p>

  %if action is 'event_edit':
    <p class='byline'>
      Created by: ${event.user.givenname} ${event.user.surname} (${event.user.email}) @ ${event.created.date()}
      %if event.updated:
        | updated @ ${event.updated.date()}
      %endif
    </p>
  %endif

  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
