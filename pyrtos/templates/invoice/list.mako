<%inherit file="pyrtos:templates/invoice/base.mako"/>

%if searchpage:
  <form action="${request.route_url('invoices_search')}" method="GET">
    ${form.csrf_token}
    %for error in form.query.errors:
      <p class=error>${error}</p>
    %endfor
    <p>
      ${form.query.label}<br />
      ${form.query}
    </p>

    %for error in form.categories.errors:
      <p class=error>${error}</p>
    %endfor
    <p>
      ${form.categories.label}<br />
      ${form.categories}
    </p>

    %for error in form.creditors.errors:
      <p class=error>${error}</p>
    %endfor
    <p>
      ${form.creditors.label}<br />
      ${form.creditors}
    </p>

    %for error in form.fromdate.errors:
      <p class=error>${error}</p>
    %endfor
    <p>
      ${form.fromdate.label}<br />
      ${form.fromdate}
    </p>

    %for error in form.todate.errors:
      <p class=error>${error}</p>
    %endfor
    <p>
      ${form.todate.label}<br />
      ${form.todate}
    </p>

    <p>
      <input type="submit" value="Submit" />
    </p>
  </form>
%endif
%if paginator.items:
  <div class='tablelist'>
    <table id='invoices'>
      <thead>
        <th>Title</th>
        <th>Amount</th>
        <th>Due</th>
        <th>Category</th>
        <th>Creditor</th>
        <th>Files</th>
        <th>Actions</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr class="${'archived' if item.archived else 'active'} ${'onhold' if item.on_hold else ''}">
            <td>${item.title}</td>
            <td>${item.amount}</td>
            <td>${item.due.date()}</td>
            <td>${item.category.title}</td>
            <td>${item.creditor.title}</td>
            <td>
              %if item.files:
                %for f in item.files:
                  <a href="${request.route_url('file_download', id=f.id, filename=f.filename)}">
                    <img src='${request.static_url("pyrtos:static/icons/page_white_get.png")}' title='Edit' alt='Edit' />
                  </a>
                %endfor
              %endif
            </td>
            <td class='actions'>
              %if request.can_i('edit'):
                %if item.category.private or item.creditor.private:
                  <a href="${request.route_url('invoice_edit', id=item.id, _query={'private' : '1'})}">
                %else:
                  <a href="${request.route_url('invoice_edit', id=item.id)}">
                %endif
                    <img src='${request.static_url("pyrtos:static/icons/page_white_edit.png")}' title='Edit' alt='Edit' />
                  </a>
              %endif
              %if item.archived:
                %if request.can_i('restore'):
                  <a href="${request.route_url('invoice_restore', id=item.id)}">
                    <img src='${request.static_url("pyrtos:static/icons/page_white_restore.png")}' title='Restore' alt='Restore' />
                  </a>
                %endif
              %else:
                %if request.can_i('archive'):
                  <a href="${request.route_url('invoice_archive', id=item.id)}">
                    <img src='${request.static_url("pyrtos:static/icons/page_white_delete.png")}' title='Delete' alt='Delete' />
                 </a>
                %endif
              %endif
            </td>
          </tr>
        %endfor
        %if total:
          <tr class='totalrow'>
            <td></td>
            <td colspan=3>${total[0][0]}</td>
          </tr>
        %endif
      </tbody>
    </table>
  </div>
  <div class='tablesum'>
  %if amount_sum:
    %for s in amount_sum:
      <span>Sum: ${s}</span>
    %endfor
  %endif
  </div>
  <div class='pager'>
    ${paginator.pager()}
  </div>
%else:
  <p>No invoices found.</p>
%endif
