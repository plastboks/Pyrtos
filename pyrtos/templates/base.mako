<html lang="en-US"
<head>
  <title>PyrTos</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <link rel="shortcut icon" href="${request.static_url('pyrtos:static/favicon.ico')}" />
  <link rel="stylesheet" href="${request.static_url('pyrtos:static/css/normalize.css')}" type="text/css" media="screen" charset="utf-8" />
  <link rel="stylesheet" href="${request.static_url('pyrtos:static/css/style.css')}" type="text/css" media="screen" charset="utf-8" />
</head>
<body>
  <div id="wrapper">
    <div id="messages">
      <%include file="pyrtos:templates/messages.mako"/>
    </div>
    <div class="sidebar corners5px">
      <%include file="pyrtos:templates/sidebar.mako"/>
    </div>
    <div id="content" class="corners5px">
       ${next.body()} 
    </div>
  </div>
</body>
</html>
