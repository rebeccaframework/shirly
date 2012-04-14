<%inherit file="project_layout.mak" />
<%block name="breadcrumb">
${h.breadcrumb([
(request.route_url('top'), 'TOP'),
(request.route_url('projects'), 'Projects'),
project_name,
])}
</%block>

<h2>Description</h2>
${description|n}
</div>
