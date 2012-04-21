<!DOCTYPE html>
<html>
<%python

from js.bootstrap import bootstrap
bootstrap.need()
%>
<head>
</head>
<body>
<div class="navbar navbar-fixed=top">
<div class="navbar-inner">
<div class="container">
<a class="brand" href="#">Shirly</a>
</div>
</div>
</div>

<div class="container">
<form method="POST" action="${request.route_url('login')}" class="form-horizontal">
<fieldset>
<legend>Login</legend>

<div class="control-group">
<label for="login" class="control-label">User Name</label>
<div class="controls">
<input type="text" name="login" id="login" />
</div>
</div>

<div class="control-group">
<label for="password" class="control-label">Password</label>
<div class="controls">
<input type="password" id="password" name="password" />
</div>
</div>
<button type="submit" class="btn btn-primary">Login</button>
</fieldset>
</form>
</div>
</body>
</html>
