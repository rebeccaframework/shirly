<%inherit file="base.mak" />
<ul class="breadcrumb">
<li><a href="${request.route_url('top')}">Top</a><span class="divider">/</span></li>
<li><a href="${request.route_url('projects')}">Projects</a><span class="divider">/</span></li>
<li><a href="${request.route_url('project', project_name=project_name)}">${project_name}</a><span class="divider">/</span></li>
<li class="active">Tickets</li>
</ul>

<div class="span3">
</div>
<div class="span9">
<h2>Tickts</h2>
<a class="btn btn-primary" href="${request.route_url('project_new_ticket', project_name=project_name)}"><i class="icon-edit"></i>new</a>

<table class="table table-striped">
<tr>
<th>#</th>
<th>Name</th>
</tr>
%for t in tickets:
<tr>
<td><a href="${request.route_url('project_ticket', project_name=project_name, ticket_no=t['ticket_no'])}">${t['ticket_no']}</a></td>
<td><a href="${request.route_url('project_ticket', project_name=project_name, ticket_no=t['ticket_no'])}">${t['ticket_name']}</a></td>
</tr>
%endfor
</table>
</div>
