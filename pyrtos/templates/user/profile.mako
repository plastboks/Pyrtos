<%inherit file="pyrtos:templates/user/base.mako" />

<form action="${request.route_url(action)}" method="POST">
  ${form.csrf_token}

  %for error in form.email.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.email.label}<br />
    ${form.email}
  </p>

  %for error in form.cellphone.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.cellphone.label}<br />
    ${form.cellphone}
  </p>

  %for error in form.givenname.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.givenname.label}<br />
    ${form.givenname}
  </p>

  %for error in form.surname.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.surname.label}<br />
    ${form.surname}
  </p>

  %for error in form.password.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.password.label}<br />
    ${form.password}
  </p>

  <p>
    ${form.confirm.label}<br />
    ${form.confirm}
  </p>

  <p class='byline'>
    Created @: ${user.created.date()}
    %if user.updated:
      | updated @ ${user.updated.date()}
    %endif
  </p>

  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
