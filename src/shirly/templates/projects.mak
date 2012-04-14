<%inherit file="layout.mak" />
<%block name="breadcrumb">
${h.breadcrumb([
(request.route_url('top'), 'TOP'),
'Projects',
])}
</%block>

<ul class="nav">
%for p in projects:
<li>
<a href="${request.route_url('project', project_name=p['project_name'])}">${p['project_name']}</a>
</li>
%endfor
</ul>
