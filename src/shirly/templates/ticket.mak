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
<%block name="extra_scripts">
<script>
$(function() {tinyMCE.init({mode: 'textareas', theme: 'advanced'});})
</script>
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
<dt>estimated time</dt>
<dd>${ticket.estimated_time}</dd>
</div>
<div>
<h2>Description</h2>
${description|n}
</div>
<div>

${renderer.begin(h.ticket_url(request, ticket), class_="form-horizontal")}
<a href="javascript:$('#ticket-form').toggle()">edit</a>
<fieldset id="ticket-form" style="display: none;" class="well">
${renderer.textfield('ticket_name')}
${renderer.textfield('estimated_time')}
${renderer.textareafield('description')}
<input type="submit" name="update" value="Update" class="btn btn-primary" />
</fieldset>
${renderer.end()}

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
