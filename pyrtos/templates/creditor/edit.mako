<%inherit file="pyrtos:templates/creditor/base.mako" />
<form action="${request.route_url(action, id=id)}" method="POST">
  ${form.csrf_token}
  %if action == 'creditor_edit':
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
  
  %if action is 'creditor_edit':
    <p class='byline'>
      Created by: ${creditor.user.givenname} ${creditor.user.surname} (${creditor.user.email}) @ ${creditor.created.date()}
      %if creditor.updated:
        | updated @ ${creditor.updated.date()}
      %endif
    </p>
  %endif

  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
