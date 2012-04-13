<%inherit file="base.mak" />
<%block name="extra_scripts">
<script>
$(function() {tinyMCE.init({mode: 'textareas', theme: 'advanced'});})
</script>
</%block>
${renderer.errorlist()}
${renderer.begin(request.route_url('new_project'), class_="form-horizontal")}
<fieldset>
<legend>New Project</legend>

<div class="control-group">
${renderer.label('project_name', class_="control-label")}
<div class="controls">
${renderer.text('project_name')}
</div>
</div>

<div class="control-group">
${renderer.label('description', class_="control-label")}
<div class="controls">
${renderer.textarea('description')}
</div>
</div>

<div class="control-group">
${renderer.label('members', class_="control-label")}
<div class="controls">
%for user_id, user_name in users:
${renderer.checkbox("member", value=user_id, id="member-%d" % user_id)}
${renderer.label("member-%d" % user_id, user_name)}
%endfor
</div>
</div>

<div class="form-actions">
<button type="submit" class="btn btn-primary">Create</button>
<button type="submit" class="btn">Cancel</button>
</div>
${renderer.end()}
</fieldset>
