<html lang="en-US"
<head>
  <title>PyrTos</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <link rel="shortcut icon" href="${request.static_url('pyrtos:static/favicon.ico')}" />
  <link rel="stylesheet" href="${request.static_url('pyrtos:static/css/normalize.css')}" type="text/css" media="screen" charset="utf-8" />
  <link rel="stylesheet" href="${request.static_url('pyrtos:static/css/login.css')}" type="text/css" media="screen" charset="utf-8" />
</head>
<body>
  <div id="login">
    <h1>Login</h1>
    <form action="${request.route_url('login')}" method="post">
      <p>
        <label>User</label>
        <input type="text" name="email">
      </p>
      <p>
        <label>Password</label>
        <input type="password" name="password">
      </p>
        <input type="submit" value="Sign in">
    </form>
  </div>
</body>
</html>
