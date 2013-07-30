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
    <label>${form.title.label}</label><br />
    ${form.title}
  </p>

  %for error in form.from_date.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    <label>${form.from_date.label}</label><br />
    ${form.from_date}
  </p>

  %for error in form.to_date.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    <label>${form.to_date.label}</label><br />
    ${form.to_date}
  </p>

  <p>
    <label>${form.private.label}</label>
    ${form.private}
  </p>

  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
