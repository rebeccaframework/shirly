<%inherit file="project_layout.mak" />
<%block name="breadcrumb">
${h.breadcrumb([(request.route_url('top'), 'TOP'), 
    (request.route_url('projects'), 'Projects'), 
    (request.route_url('project', project_name=project_name), project_name), 
    'Tickets'])}
</%block>

<h2>Tickets</h2>
<a class="btn btn-primary" href="${request.route_url('project_new_ticket', project_name=project_name)}"><i class="icon-edit"></i>new</a>

<table class="table table-striped">
<thead>
<tr>
<th>#</th>
<th>Name</th>
</tr>
</thead>
<tbody>
%for t in tickets:
<tr>
<td><a href="${request.route_url('project_ticket', project_name=project_name, ticket_no=t['ticket_no'])}">${t['ticket_no']}</a></td>
<td><a href="${request.route_url('project_ticket', project_name=project_name, ticket_no=t['ticket_no'])}">${t['ticket_name']}</a></td>
</tr>
</tbody>
%endfor
</table>
