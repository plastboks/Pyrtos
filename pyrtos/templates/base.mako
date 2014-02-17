<html lang="en-US"
<head>
  <title>${request.registry.settings.get('pyrtos.title')}</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <link rel="shortcut icon" href="${request.static_url('pyrtos:static/favicon.ico')}" />
  <link rel="stylesheet" href="${request.static_url('pyrtos:static/css/normalize.css')}" type="text/css" media="screen" charset="utf-8" />
  <link rel="stylesheet" href="${request.static_url('pyrtos:static/css/style.css')}" type="text/css" media="screen" charset="utf-8" />
</head>
<body>
  <section id="wrapper">
    <header>
       <h1>${request.registry.settings.get('pyrtos.title')}</h1>
    </header>
    <section id="messages">
      <%include file="pyrtos:templates/messages.mako"/>
    </section>
    <section class="sidebar corners5px">
      <%include file="pyrtos:templates/sidebar.mako"/>
    </section>
    <section id="content" class="corners5px">
       ${next.body()} 
    </section>
    <section id='footer'>
      <p>${request.registry.settings.get('pyrtos.footer')}</p>
    </section>
  </section>
</body>
</html>
