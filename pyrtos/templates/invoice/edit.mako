<%inherit file="pyrtos:templates/invoice/base.mako" />
  %if not private and action is not 'invoice_edit':
    <p class='changestate'>
      Want to create a private invoice? <a href="${request.current_route_url(_query={'private': '1'})}">Click here.</a>
    </p>
  %endif
  %if action is 'invoice_edit' and not private:
    <p class='changestate'>
      Want to make this invoice private? <a href="${request.current_route_url(_query={'private': '1'})}">Click here.</a>
    </p>
  %endif
  %if action is 'invoice_edit' and private:
    <p class='changestate'>
      Want to make this invoice shared? <a href="${request.current_route_url()}">Click here.</a>
    </p>
  %endif

%if private:
  <form action="${request.route_url(action, id=id, _query={'private' : '1'})}" method="POST">
%else:
  <form action="${request.route_url(action, id=id)}" method="POST">
%endif

  ${form.csrf_token}
  %if action == 'invoice_edit':
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
    <label>${form.creditor_id.label}</label>
    ${form.creditor_id}
  </p>

  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
