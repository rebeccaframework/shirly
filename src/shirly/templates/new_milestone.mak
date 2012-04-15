<%inherit file="project_layout.mak" />
<%block name="extra_scripts">
<script>
$(function() {
    tinyMCE.init({mode: 'textareas', theme: 'advanced'});
    $('.date').datepicker();
})
</script>
</%block>

<%block name="breadcrumb">
<ul class="breadcrumb">
<li><a href="${request.route_url('top')}">Top</a><span class="divider">/</span></li>
<li><a href="${request.route_url('projects')}">Projects</a><span class="divider">/</span></li>
<li><a href="${request.route_url('project', project_name=project_name)}">${project_name}</a><span class="divider">/</span></li>
<li class="active">New Milestone</li>
</ul>
</%block>

${renderer.errorlist()}
${renderer.begin(request.route_url('project_new_milestone', project_name=project_name), class_="form-horizontal")}
<fieldset>
<legend>New Milestone</legend>
<div class="control-group">
${renderer.label('milestone', class_="control-label")}
<div class="controls">
${renderer.text('milestone_name')}
</div>
</div>

<div class="control-group">
${renderer.label('due_date', class_="control-label")}
<div class="controls">
${renderer.text('due_date', class_="date")}
</div>
</div>

<div class="control-group">
${renderer.label('description', class_="control-label")}
<div class="controls">
${renderer.textarea('description')}
</div>
</div>

<div class="form-actions">
<button type="submit" class="btn btn-primary">Create</button>
<button type="submit" class="btn">Cancel</button>
</div>

</fieldset>
${renderer.end()}
