<%inherit file="pyrtos:templates/file/base.mako" />
<form action="${request.route_url(action, id=id)}" method="POST" enctype="multipart/form-data">
  ${form.csrf_token}
  %if action == 'file_edit':
    ${form.id()}
  %endif

  %for error in form.title.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.title.label}<br />
    ${form.title}
  </p>

  %for error in form.private.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.private.label}
    ${form.private}
  </p>

  %for error in form.file.errors:
    <p class=error>${error}</p>
  %endfor
  <p>
    ${form.file.label}
    ${form.file}
  </p>

  <p>
    <input type="submit" value="Submit" />
  </p>
</form>
