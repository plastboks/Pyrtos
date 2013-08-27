<%inherit file="pyrtos:templates/alertsetting/base.mako" />
<form action="${request.route_url(action, id=id)}" method="POST">
  ${form.csrf_token}
  %if action == 'alertsetting_edit':
    ${form.id()}
  %endif

  %for error in form.title.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.title.label}:
    ${form.title}
  </p>

  %for error in form.weekfilter.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.weekfilter.label}:
    ${form.weekfilter}
  </p>

  %for error in form.hour.errors:
    <p class=error>${error}</p>
  %endfor
  %for error in form.minute.errors:
    <p class=error>${error}</p>
  %endfor
  %for error in form.days_in_advance.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.hour.label}:
    ${form.hour}
    ${form.minute.label}:
    ${form.minute}
    ${form.days_in_advance.label}:
    ${form.days_in_advance}
  </p>

  %for error in form.active.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.active.label}:
    ${form.active}
  </p>

  %if action is 'alertsetting_edit':
    <p class='byline'>
      Created by: ${alertsetting.user.givenname} ${alertsetting.user.surname} (${alertsetting.user.email}) @ ${alertsetting.created.date()}
      %if alertsetting.updated:
        | updated @ ${alertsetting.updated.date()}
      %endif
    </p>
  %endif
  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
