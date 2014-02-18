<%inherit file="pyrtos:templates/file/base.mako"/>

%if paginator.items:
  <section class='tablelist'>
    <table id='files'>
      <thead>
        <th>Title</th>
        <th>Private</th>
        <th>Downloads</th>
      </thead>
      <tbody>
        %for item in paginator.items:
          <tr>
            <td>${item.title}</td>
            <td>${item.private}</td>
            <td>
            %if item.filename:
                <a href="${request.route_url('file_download', id=item.id, filename=item.filename)}">Download</a>
            %endif
            </td>
          </tr>
        %endfor
      </tbody>
    </table>
  </section>
  <section class='pager'>
    ${paginator.pager()}
  </section>
%else:
  <p>No files found.</p>
%endif
