<%inherit file="pyrtos:templates/invoice/base.mako"/>

%if items:
  %for cat,invoices in items.iteritems():
    <h2>${cat}</h2>
    <div class='tablelist'>
      <table class='invoices'>
        <thead>
          <th>Title</th>
          <th>Amount</th>
          <th>Category</th>
          <th>Creditor</th>
          <th>Actions</th>
        </thead>
        <tbody>
          %for item in invoices[0]:
            <tr>
              <td>${item.title}</td>
              <td>${item.amount}</td>
              <td>${item.category.title}</td>
              <td>${item.creditor.title}</td>
              <td class='actions'>
                %if request.can_i('edit'):
                  %if private:
                    <a href="${request.route_url('invoice_edit', id=item.id, _query={'private' : '1'})}">
                  %else:
                    <a href="${request.route_url('invoice_edit', id=item.id)}">
                  %endif
                      <img src='${request.static_url("pyrtos:static/icons/page_white_edit.png")}' title='Edit' alt='Edit' />
                  </a>
                %endif
                %if archived:
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
            <tr class='totalrow'>
              <td></td>
              <td colspan=3>${invoices[1][0]}</td>
            </tr>
        </tbody>
      </table>
    </div>
  %endfor
%else:
  <p>No invoices found.</p>
%endif
