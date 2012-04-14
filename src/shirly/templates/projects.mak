<%inherit file="base.mak" />
${h.breadcrumb([
(request.route_url('top'), 'TOP'),
'Projects',
])}

<ul class="nav">
%for p in projects:
<li>
<a href="${request.route_url('project', project_name=p['project_name'])}">${p['project_name']}</a>
</li>
%endfor
</ul>
