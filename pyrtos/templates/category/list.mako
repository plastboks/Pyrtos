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
              %if request.can_i('edit'):
                <a href="${request.route_url('category_edit', id=item.id)}">Edit</a>
              %endif
              %if archived:
                %if request.can_i('restore'):
                  <a href="${request.route_url('category_restore', id=item.id)}">Restore</a>
                %endif
              %else:
                %if request.can_i('archive'):
                  <a href="${request.route_url('category_archive', id=item.id)}">Archive</a>
                %endif
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
