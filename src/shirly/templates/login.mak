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
<form method="POST" action="${request.route_url('login')}" class="form-inline">
<fieldset>
<legend>Login</legend>
<label for="login">User Name</label>
<input type="text" name="login" id="login" />
<label for="password">Password</label>
<input type="password" id="password" name="password" />
<button type="submit" class="btn btn-primary">Login</button>
</fieldset>
</form>
</div>
</body>
</html>
