<h2><a href="${request.route_url('project_milestones', project_name=project_name)}">Milestones</a></h2>
<div class="well">
<ul class="nav">
%for m in milestones:
<li><a href="#">${m['milestone_name']} ${m['due_date'].strftime('%Y-%m-%d')}</a></li>
%endfor
</ul>

<a class="btn btn-primary" href="${request.route_url('project_new_milestone', project_name=project_name)}">New</a>
</div>
