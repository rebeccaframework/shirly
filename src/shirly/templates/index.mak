<h1>Shirly</h1>
${request.authenticated_user.user_name}
<a href="${request.route_url('logout')}">Logout</a>
<a href="${request.route_url('new_project')}">New Project</a>

<div>
<h2>Projects</h2>
<ul>
%for project in projects:
<li><a href="${request.route_url('project', project_name=project['project_name'])}">${project['project_name']}</a></li>
%endfor
</ul>
</div>
