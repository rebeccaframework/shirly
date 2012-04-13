<%inherit file="base.mak" />
<ul class="breadcrumb">
<li><a href="${request.route_url('top')}">Top</a><span class="divider">/</span></li>
<li class="active">Projects</li>
</ul>

<ul class="nav">
%for p in projects:
<li>
<a href="${request.route_url('project', project_name=p['project_name'])}">${p['project_name']}</a>
</li>
%endfor
</ul>
