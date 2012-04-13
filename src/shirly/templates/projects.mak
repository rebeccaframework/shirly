<ul>
%for p in projects:
<li>
<a href="${request.route_url('project', project_name=p['project_name'])}">${p['project_name']}</a>
</li>
%endfor
</ul>
