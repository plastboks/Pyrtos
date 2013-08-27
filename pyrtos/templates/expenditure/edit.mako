<%inherit file="pyrtos:templates/expenditure/base.mako" />
  %if not private and action is not 'expenditure_edit':
    <p class='changestate'>
      Want to create a private expenditure? <a href="${request.current_route_url(_query={'private': '1'})}">Click here.</a>
    </p>
  %endif
  %if action is 'expenditure_edit' and not private:
    <p class='changestate'>
      Want to make this expenditure private? <a href="${request.current_route_url(_query={'private': '1'})}">Click here.</a>
    </p>
  %endif
  %if action is 'expenditure_edit' and private:
    <p class='changestate'>
      Want to make this expenditure shared? <a href="${request.current_route_url()}">Click here.</a>
    </p>
  %endif

%if private:
  <form action="${request.route_url(action, id=id, _query={'private' : '1'})}" method="POST">
%else:
  <form action="${request.route_url(action, id=id)}" method="POST">
%endif

  ${form.csrf_token}
  %if action is 'expenditure_edit':
    ${form.id()}
  %endif

  %for error in form.title.errors:
    <p class=error>${error}</p>
  %endfor

  <p>
    ${form.title.label}<br />
    ${form.title}
  </p>

  %for error in form.amount.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.amount.label}<br />
    ${form.amount}
  </p>

  <p>
    ${form.category_id.label}
    ${form.category_id}
  </p>

  %if action is 'expenditure_edit':
    <p class='byline'>
      Created by: ${expenditure.user.givenname} ${expenditure.user.surname} (${expenditure.user.email}) @ ${expenditure.created.date()}
      %if expenditure.updated:
        | updated @ ${expenditure.updated.date()}
      %endif
    </p>
  %endif

  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
