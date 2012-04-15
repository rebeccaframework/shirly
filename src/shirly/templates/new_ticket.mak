<%inherit file="project_layout.mak" />
<%block name="extra_scripts">
<script>
$(function() {tinyMCE.init({mode: 'textareas', theme: 'advanced'});})
</script>
</%block>
<%block name="breadcrumb">
${h.breadcrumb([
(request.route_url('top'), "TOP"),
(request.route_url('projects'), "Projects"),
(request.route_url('project', project_name=project_name), project_name),
"New Ticket",
])}
</%block>


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
