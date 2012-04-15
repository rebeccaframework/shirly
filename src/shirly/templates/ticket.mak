<%inherit file="project_layout.mak" />
<%block name="breadcrumb">
${h.breadcrumb([
(request.route_url('top'), 'TOP'),
(request.route_url('projects'), 'Projects'),
(request.route_url('project', project_name=project_name), project_name),
(request.route_url('project_tickets', project_name=project_name), 'Tickets'),
"%s&nbsp;%s" % (ticket_no, ticket_name),
])}
</%block>

<h1>#${ticket_no} ${ticket_name}</h1>
<div class="well">
<dl>
<dt>reported by </dt>
<dd>${reporter_name}</dd>
<dt>status</dt>
<dd>${status}</dd>
</div>
<div>
<h2>Description</h2>
${description|n}
</div>
<div>
<form action="${request.url}" method="POST">
<input type="hidden" name="status" value="finished" />
<button type="submit">Finish</button>
</form>
<form action="${request.url}" method="POST">
<input type="hidden" name="status" value="closed" />
<button type="submit">Close</button>
</form>
</div>
</ul>
