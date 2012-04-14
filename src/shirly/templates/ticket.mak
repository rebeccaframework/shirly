<%inherit file="base.mak" />
<ul class="breadcrumb">
<li><a href="${request.route_url('top')}">Top</a><span class="divider">/</span></li>
<li><a href="${request.route_url('projects')}">Projects</a><span class="divider">/</span></li>
<li><a href="${request.route_url('project', project_name=project_name)}">${project_name}</a><span class="divider">/</span></li>
<li><a href="${request.route_url('project_tickets', project_name=project_name)}">Tickets</a><span class="divider">/</span></li>
<li class="active">#${ticket_no}&nbsp;${ticket_name}</li>
<h2>#${ticket_no} ${ticket_name}</h2>
<div>
${description|n}
</div>
</ul>
