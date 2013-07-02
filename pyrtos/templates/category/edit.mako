<%inherit file="pyrtos:templates/base.mako" />
<h1>${title}</h1>
<form action="${request.route_url(action, id=id)}" method="POST">

  %if action == 'category_edit':
    ${form.id()}
  %endif

  %for error in form.title.errors:
    <p class=error>${error}</p>
  %endfor

  <p>
    <label>${form.title.label}</label><br />
    ${form.title}
  </p>

  <p>
    <label>${form.name.label}</label><br />
    ${form.name}
  </p>

  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
