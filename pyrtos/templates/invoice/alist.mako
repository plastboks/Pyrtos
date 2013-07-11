<%inherit file="pyrtos:templates/invoice/base.mako"/>

%if paiditems:
  <h2>Paid invoices for: ${year}-${month}</h2>
  %for cat,invoices in paiditems.iteritems():
    <div class='tablelist'>
      <table class='invoices'>
        <thead>
          <th>Title</th>
          <th>Amount</th>
          <th>Due</th>
          <th>Paid</th>
          <th>Category</th>
          <th>Creditor</th>
          <th>Actions</th>
        </thead>
        <tbody>
          %for item in invoices[0]:
            <tr>
              <td>${item.title}</td>
              <td>${item.amount}</td>
              <td>${item.due.date()}</td>
              <td>
                %if item.paid:
                  ${item.paid.date()}
                %endif
              </td>
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
  <p>No paid invoices found.</p>
%endif
%if unpaiditems:
  <h2>Unpaid invoices</h2>
  %for cat,invoices in unpaiditems.iteritems():
    <div class='tablelist'>
      <table class='invoices unpaid'>
        <thead>
          <th>Title</th>
          <th>Amount</th>
          <th>Due</th>
          <th>Category</th>
          <th>Creditor</th>
          <th>Actions</th>
        </thead>
        <tbody>
          %for item in invoices[0]:
            <tr class='${item.css_class_for_time_distance()}'>
              <td>${item.title}</td>
              <td>${item.amount}</td>
              <td>
                ${item.time_to_expires_in_words()}
              </td>
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
                  <a href="${request.route_url('invoice_quickpay', id=item.id)}">
                      <img src='${request.static_url("pyrtos:static/icons/page_white_go.png")}' title='Quickpay' alt='Quickpay' />
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
%endif
