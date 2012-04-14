<%inherit file="base.mak" />
<%block name="extra_scripts">
<script>
$(function() {tinyMCE.init({mode: 'textareas', theme: 'advanced'});})
</script>
</%block>

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
${renderer.errorlist()}
${renderer.begin(request.route_url('project_new_ticket', project_name=project_name), class_="form-horizontal")}
<fieldset>
<legend>New Ticket</legend>

<div class="control-group">
${renderer.label('ticket', class_="control-label")}
<div class="controls">
${renderer.text('ticket_name')}
</div>
</div>

<div class="control-group">
${renderer.label('description', class_="control-label")}
<div class="controls">
${renderer.textarea('description')}
</div>
</div>

<div class="control-group">
${renderer.label('estimated_time', class_="control-label")}
<div class="controls">
${renderer.text('estimated_time')}
</div>
</div>

<div class="form-actions">
<button type="submit" class="btn btn-primary">Create</button>
<button type="submit" class="btn">Cancel</button>
</div>
</fieldset>
${renderer.end()}
</div>
