<%inherit file="pyrtos:templates/category/base.mako" />
<form action="${request.route_url(action, id=id)}" method="POST">
  ${form.csrf_token}
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
    <label>${form.private.label}</label>
    ${form.private}
  </p>

  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
