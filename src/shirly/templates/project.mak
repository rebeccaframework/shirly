<%inherit file="base.mak" />
<ul class="breadcrumb">
<li><a href="${request.route_url('top')}">Top</a><span class="divider">/</span></li>
<li><a href="${request.route_url('projects')}">Projects</a><span class="divider">/</span></li>
<li class="active">${project_name}</li>
</ul>

<div class="row">
<div class="span4">
<h2>Members</h2>
<ul>
%for m in members:
<li>${m['user_name']}</li>
%endfor
</ul>
</div>

<div class="span8">
<h2>Description</h2>
${description|n}
</div>
</div>
