<%inherit file="base.mak" />
${h.breadcrumb([
(request.route_url('top'), 'TOP'),
(request.route_url('projects'), 'Projects'),
(request.route_url('project', project_name=project_name), project_name),
(request.route_url('project_tickets', project_name=project_name), 'Tickets'),
"%s&nbsp;%s" % (ticket_no, ticket_name),
])}

<h1>#${ticket_no} ${ticket_name}</h1>
<div>
<h2>Description</h2>
${description|n}
</div>
</ul>
