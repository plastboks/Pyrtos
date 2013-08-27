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
    ${form.title.label}<br />
    ${form.title}
  </p>

  %for error in form.amount.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.amount.label}<br />
    ${form.amount}
  </p>

  <p>
    ${form.user_id.label}
    ${form.user_id}
  </p>

  %if action is 'income_edit':
    <p class='byline'>
      Created by: ${income.user.givenname} ${income.user.surname} (${income.user.email}) @ ${income.created.date()}
      %if income.updated:
        | updated @ ${income.updated.date()}
      %endif
    </p>
  %endif
  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
