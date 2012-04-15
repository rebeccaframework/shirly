<h2><a href="${request.route_url('project_tickets', project_name=project_name)}">Tickets</a></h2>
<div class="well">
<ul class="nav">
%for t in tickets:
<li><a href="${request.route_url('project_ticket', project_name=project_name, ticket_no=t['ticket_no'])}">${t['ticket_no']} ${t['ticket_name']}</a></li>
%endfor
</ul>
<a class="btn btn-primary" href="${request.route_url('project_new_ticket', project_name=project_name)}"><i class="icon-edit"></i>new</a>
</div>
