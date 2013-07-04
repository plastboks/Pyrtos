<%inherit file="pyrtos:templates/user/base.mako" />

<form action="${request.route_url(action, id=id)}" method="POST">
  ${form.csrf_token}
  %if action == 'user_edit':
    ${form.id()}
  %endif

  %for error in form.email.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    <label>${form.email.label}</label><br />
    ${form.email}
  </p>

  %for error in form.givenname.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    <label>${form.givenname.label}</label><br />
    ${form.givenname}
  </p>
  
  %for error in form.surname.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    <label>${form.surname.label}</label><br />
    ${form.surname}
  </p>

  %for error in form.password.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    <label>${form.password.label}</label><br />
    ${form.password}
  </p>

  <p>
    <label>${form.confirm.label}</label><br />
    ${form.confirm}
  </p>

  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
