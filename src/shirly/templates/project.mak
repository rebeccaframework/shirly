<%inherit file="base.mak" />
${h.breadcrumb([
(request.route_url('top'), 'TOP'),
(request.route_url('projects'), 'Projects'),
project_name,
])}

<div class="row">
<div class="span3">
<h2>Members</h2>
<ul>
%for m in members:
<li>${m['user_name']}</li>
%endfor
</ul>
<h2><a href="${request.route_url('project_tickets', project_name=project_name)}">Tickets</a></h2>
<a class="btn btn-primary" href="${request.route_url('project_new_ticket', project_name=project_name)}"><i class="icon-edit"></i>new</a>
<ul class="nav">
%for t in tickets:
<li><a href="${request.route_url('project_ticket', project_name=project_name, ticket_no=t['ticket_no'])}">${t['ticket_no']} ${t['ticket_name']}</a></li>
%endfor
</ul>
</div>

<div class="span9">
<h2>Description</h2>
${description|n}
</div>
</div>
