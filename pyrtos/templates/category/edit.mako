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

  %if action is 'category_edit':
    <p class='byline'>
      Created by: ${category.user.givenname} ${category.user.surname} (${category.user.email}) @ ${category.created.date()}
      %if category.updated:
        | updated @ ${category.updated.date()}
      %endif
    </p>
  %endif

  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
