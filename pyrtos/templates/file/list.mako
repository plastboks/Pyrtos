<%inherit file="pyrtos:templates/file/base.mako"/>

%if paginator.items:
  <div class='tablelist'>
    <table id='files'>
      <thead>
        <th>Title</th>
        <th>Downloads</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr>
            <td>${item.title}</td>
            <td>
            %if item.filename:
                <a href="${request.route_url('file_download', id=item.id)}">Download</a></td>
            %endif
          </tr>
        %endfor
      </tbody>
    </table>
  </div>
  <div class='pager'>
    ${paginator.pager()}
  </div>
%else:
  <p>No files found.</p>
%endif
