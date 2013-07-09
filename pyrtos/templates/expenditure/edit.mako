<%inherit file="pyrtos:templates/expenditure/base.mako" />
<p>
  %if not private and action is not 'expenditure_edit':
    Want to create a private expenditure? <a href="${request.route_url('expenditure_new', _query={'private': '1'})}">Click here.</a>
  %endif
</p>
%if private:
  <form action="${request.route_url(action, id=id, _query={'private' : '1'})}" method="POST">
%else:
  <form action="${request.route_url(action, id=id)}" method="POST">
%endif

  ${form.csrf_token}
  %if action == 'expenditure_edit':
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
    <label>${form.amount.label}</label><br />
    ${form.amount}
  </p>

  <p>
    <label>${form.category_id.label}</label>
    ${form.category_id}
  </p>

  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
