<%inherit file="pyrtos:templates/tag/base.mako"/>

%if tags:
  %for tag in tags:
    <span>${tag}</span>
  %endfor
%else:
  <p>No tags found.</p>
%endif
