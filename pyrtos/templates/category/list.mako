<%inherit file="pyrtos:templates/base.mako"/>

<h1>${title}</h1>
<div class="upper_toolbar">
  <ul>
    <li><a href="${request.route_url('category_new')}">New</a></li>
  </ul>
</div>

%if paginator.items:
  <div class='tablelist'>
    <table id='categories'>
      <thead>
        <th>Title</th>
        <th>Actions</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr>
            <td>${item.title}</td>
            <td><a href="${request.route_url('category_edit', id=item.id)}">Edit</a></td>
          </tr>
        %endfor
      </tbody>
    </table>
  </div>
  ${paginator.pager()}
%else:
  <p>No categories found.</p>
%endif
