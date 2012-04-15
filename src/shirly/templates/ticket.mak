<%inherit file="project_layout.mak" />
<%block name="breadcrumb">
${h.breadcrumb([
(request.route_url('top'), 'TOP'),
(request.route_url('projects'), 'Projects'),
(request.route_url('project', project_name=project_name), project_name),
(request.route_url('project_tickets', project_name=project_name), 'Tickets'),
"%s&nbsp;%s" % (ticket_no, ticket_name),
])}
</%block>

<h1>#${ticket_no} ${ticket_name}</h1>
<div class="well">
<dl>
<dt>reported by </dt>
<dd>${reporter_name}</dd>
<dt>owner </dt>
<dd>${owner_name}</dd>
<dt>status</dt>
<dd>${status}</dd>
</div>
<div>
<h2>Description</h2>
${description|n}
</div>
<div>

<form action="${request.url}" method="POST">
<fieldset>
<legend>Operations</legend>
<div class="form-actions">
<label>Assgin To</label>
<select name="owner">
%for u in members:
<option value="${u[0]}">${u[1]}</option>
%endfor
</select>
<div class="btn-group">
<input type="submit" name="operation" value="Reopen" class="btn" />
<input type="submit" name="operation" value="Assign" class="btn" />
<input type="submit" name="operation" value="Accept" class="btn" />
<input type="submit" name="operation" value="Finish" class="btn" />
<input type="submit" name="operation" value="Close" class="btn" />
</div>
</fieldset>
</div>
</form>
</div>
</ul>
