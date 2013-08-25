<html lang="en-US"
<head>
  <title>${request.registry.settings.get('pyrtos.title')}</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <link rel="shortcut icon" href="${request.static_url('pyrtos:static/favicon.ico')}" />
  <link rel="stylesheet" href="${request.static_url('pyrtos:static/css/normalize.css')}" type="text/css" media="screen" charset="utf-8" />
  <link rel="stylesheet" href="${request.static_url('pyrtos:static/css/login.css')}" type="text/css" media="screen" charset="utf-8" />
</head>
<body>
  <div id="login">
    <h1>${request.registry.settings.get('pyrtos.title')}</h1>
    <form action="${request.route_url('login')}" method="post">
      ${form.csrf_token}
      %for m in request.session.pop_flash('error'):
        <p class='error'>${m}<p>
      %endfor
      %for error in form.email.errors:
        <p class='error'>${error}</p>
      %endfor
      <p>
        ${form.email.label}<br />
        ${form.email}
      </p>
      <p>
        ${form.password.label}<br />
        ${form.password}
      </p>
        <input type="submit" value="Login">
    </form>
  </div>
</body>
</html>
