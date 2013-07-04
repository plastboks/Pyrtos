<%inherit file="pyrtos:templates/category/base.mako"/>

%if paginator.items:
  <div class='tablelist'>
    <table id='categories'>
      <thead>
        <th>Title</th>
        <th>Name</th>
        <th>Actions</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr>
            <td>${item.title}</td>
            <td>${item.name}</td>
            <td class='actions'>
              <a href="${request.route_url('category_edit', id=item.id)}">Edit</a>
              %if archived:
                <a href="${request.route_url('category_restore', id=item.id)}">Restore</a>
              %else:
                <a href="${request.route_url('category_delete', id=item.id)}">Archive</a>
              %endif
            </td>
          </tr>
        %endfor
      </tbody>
    </table>
  </div>
  ${paginator.pager()}
%else:
  <p>No categories found.</p>
%endif
