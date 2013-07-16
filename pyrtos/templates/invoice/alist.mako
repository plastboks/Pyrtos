<%inherit file="pyrtos:templates/invoice/base.mako"/>

%if paiditems:
  <h2>Paid invoices for: ${year}-${"%02d" % month}</h2>
  %for cat,invoices in paiditems.iteritems():
    <div class='tablelist'>
      <table class='invoices'>
        <thead>
          <th>Title</th>
          <th>Amount</th>
          <th>Expired</th>
          <th>Paid</th>
          <th>Category</th>
          <th>Creditor</th>
          <th>Files</th>
          <th>Actions</th>
        </thead>
        <tbody>
          %for item in invoices[0]:
            <tr class="${'onhold' if item.on_hold else ''}">
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
              <td>
                %if item.files:
                  %for f in item.files:
                    <a href="${request.route_url('file_download', id=item.id)}">
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
              <td colspan=3>${invoices[1][0][0]}</td>
            </tr>
        </tbody>
      </table>
    </div>
  %endfor
%else:
  <p>No paid invoices found for: ${year}-${"%02d" % month}</p>
%endif
<div class='nextprev'>
  <span class='prev'>
    <a href="${request.current_route_url(_query={'year' : prevmonth[0], 'month' : prevmonth[1]})}">
      Previous month
    </a>
  </span>
  <span class='next'>
    <a href="${request.current_route_url(_query={'year' : nextmonth[0], 'month' : nextmonth[1]})}">
      Next Month
    </a>
  </span>
</div>
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
          <th>Files</th>
          <th>Actions</th>
        </thead>
        <tbody>
          %for item in invoices[0]:
            <tr class="${item.css_class_for_time_distance()} ${'onhold' if item.on_hold else ''}">
              <td>${item.title}</td>
              <td>${item.amount}</td>
              <td>
                ${item.time_to_expires_in_words()}
              </td>
              <td>${item.category.title}</td>
              <td>${item.creditor.title}</td>
              <td>
                %if item.files:
                  %for f in item.files:
                    <a href="${request.route_url('file_download', id=f.id)}">
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
              <td colspan=3>${invoices[1][0][0]}</td>
            </tr>
        </tbody>
      </table>
    </div>
  %endfor
%endif
