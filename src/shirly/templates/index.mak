<%inherit file="layout.mak" />
<%block name="breadcrumb">
${h.breadcrumb([
'TOP',
])}
</%block>

<div class="row">

<div class="span4">
<h2><a href="${request.route_url('projects')}">Projects</a></h2>
<div class="well">
<ul class="nav">
%for project in projects:
<li><a href="${request.route_url('project', project_name=project['project_name'])}">${project['project_name']}</a></li>
%endfor
</ul>
</div>
</div>

<div class="span4">
<h2>Tickets</h2>
<h3>Reported</h3>
<div class="well">
<ul class="nav">
%for t in request.authenticated_user.reported_tickets:
<li>
<a href="${request.route_url('project_ticket', project_name=t.project.project_name, ticket_no=t.ticket_no)}">
${t.ticket_name} ${t.project.project_name}</a>
</li>
</ul>
%endfor
</div>
<h3>Owned</h3>
<div class="well">
<ul class="nav">
%for t in request.authenticated_user.owned_tickets:
<li>
<a href="${request.route_url('project_ticket', project_name=t.project.project_name, ticket_no=t.ticket_no)}">
${t.ticket_name} ${t.project.project_name}</a>
</li>
</ul>
%endfor
</div>
</div>

<div class="span4">
<h2>Milestones</h2>
<div id="well">
</div>
</div>

</div>
