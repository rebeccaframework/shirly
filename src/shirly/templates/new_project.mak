<html>
<head>
<script>
$(function() {tinyMCE.init({mode: 'textareas', theme: 'advanced'});})
</script>
</head>
<body>
${renderer.errorlist()}
${renderer.begin(request.route_url('new_project'))}
<ul>
<li>
${renderer.label('project_name')}
${renderer.text('project_name')}
</li>
<li>
${renderer.label('description')}
${renderer.textarea('description')}
</li>
<li>
${renderer.label('members')}
%for user_id, user_name in users:
${renderer.checkbox("member", value=user_id, id="member-%d" % user_id)}
${renderer.label("member-%d" % user_id, user_name)}
%endfor
</li>
<li>
${renderer.submit('Create')}
</li>
</ul>
${renderer.end()}
</body>
</html>
