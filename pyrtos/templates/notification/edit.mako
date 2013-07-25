<%inherit file="pyrtos:templates/notification/base.mako" />
<form action="${request.route_url(action, id=id)}" method="POST">
  ${form.csrf_token}
  %if action == 'notification_edit':
    ${form.id()}
  %endif

  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
