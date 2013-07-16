<%inherit file="pyrtos:templates/income/base.mako" />
<form action="${request.route_url(action, id=id)}" method="POST">
  ${form.csrf_token}
  %if action == 'income_edit':
    ${form.id()}
  %endif

  %for error in form.title.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    <label>${form.title.label}</label><br />
    ${form.title}
  </p>

  %for error in form.amount.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    <label>${form.amount.label}</label><br />
    ${form.amount}
  </p>

  <p>
    <label>${form.user_id.label}</label>
    ${form.user_id}
  </p>

  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
