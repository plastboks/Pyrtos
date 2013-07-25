<%inherit file="pyrtos:templates/notification/base.mako" />
<form action="${request.route_url(action, id=id)}" method="POST">
  ${form.csrf_token}
  %if action == 'notification_edit':
    ${form.id()}
  %endif

  %for error in form.hour.errors:
    <p class=error>${error}</p>
  %endfor
  %for error in form.minute.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    <label>${form.hour.label}: </label>
    ${form.hour}
    <label>${form.minute.label}: </label>
    ${form.minute}
  </p>

  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
