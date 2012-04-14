<%inherit file="base.mak" />
${h.breadcrumb([
'TOP',
])}

<div class="row">

<div class="span4">
<h2><a href="${request.route_url('projects')}">Projects</a></h2>
<ul class="nav">
%for project in projects:
<li><a href="${request.route_url('project', project_name=project['project_name'])}">${project['project_name']}</a></li>
%endfor
</ul>
</div>

<div class="span4">
<h2>Tickets</h2>
</div>

<div class="span4">
<h2>Milestones</h2>
</div>

</div>
