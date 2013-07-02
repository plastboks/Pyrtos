<%inherit file="pyrtos:templates/base.mako"/>

<h1>${title}</h1>

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
            <td></td>
          </tr>
        %endfor
      </tbody>
    </table>
  </div>
  ${paginator.pager()}
%else:
  <p>No categories found.</p>
%endif
