<%inherit file="project_layout.mak" />
<%block name="breadcrumb">
${h.breadcrumb([(request.route_url('top'), 'TOP'), 
    (request.route_url('projects'), 'Projects'), 
    (request.route_url('project', project_name=project.project_name), project.project_name), 
    'Tickets'])}
</%block>

<h2>Tickets</h2>
<a class="btn btn-primary" href="${request.route_url('project_new_ticket', project_name=project.project_name)}"><i class="icon-edit"></i>new</a>

${h.grid(request,
    [("#", h.attrgetter('ticket_no')),
    ('Name', h.partial(h.link_to_ticket, request)),
    ('Reporter', h.attrgetter('reporter_name')),
    ('Owner', h.attrgetter('owner_name')),
    ],
    tickets,
)}
