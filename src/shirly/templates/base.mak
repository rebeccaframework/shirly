<!DOCTYPE html>
<html>
<%python

from js.bootstrap import bootstrap
bootstrap.need()
%>
<head>
<%block name="extra_scripts" />
</head>
<body>
<div class="navbar navbar-fixed=top">
<div class="navbar-inner">
<div class="container">
<a class="brand" href="${request.route_url('top')}">Shirly</a>
<ul class="nav">
<li><a href="${request.route_url('new_project')}">New Project</a></li>
</ul>
<ul class="nav pull-right">
<li><p class="navbar-text">Logged in as <strong>${request.authenticated_user.user_name}</strong></p></li>
<li><a href="${request.route_url('logout')}">Logout</a></li>
</ul>
</div>
</div>
</div>
<div class="container">
${next.body()}
</div>

</body>
</html>
