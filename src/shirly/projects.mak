<ul>
%for project in projects:
<li>
<a href="${request.route_url('project', project['project_name']}">${project['project_name']}</a>
</li>
%endfor
</ul>
