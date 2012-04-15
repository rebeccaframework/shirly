
<%inherit file="project_layout.mak" />
<%block name="breadcrumb">
${h.breadcrumb([
(request.route_url('top'), 'TOP'),
(request.route_url('projects'), 'Projects'),
(request.route_url('project', project_name=project_name), project_name),
('Milestones'),
])}
</%block>

%for m in milestones:
<div class="well">
<h2>${m['milestone_name']}</h2>
<div>
<dl>
<dt>Due Date</dt>
<dd>${m['due_date'].strftime('%Y-%m-%d')}</dd>
<dt>Tickets</dt>
<dd>${m['ticket_count']}</dd>
</dl>
</div>
<div>
${m['description']|n}
</div>
</div>
%endfor
