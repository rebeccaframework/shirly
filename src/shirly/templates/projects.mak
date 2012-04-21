<%inherit file="layout.mak" />
<%block name="breadcrumb">
${h.breadcrumb([
(request.route_url('top'), 'TOP'),
'Projects',
])}
</%block>

${h.grid(request, 
    [('Name', h.partial(h.link_to_project, request)),
        ('Tickets', h.attrgetter('active_ticket_count')),
        ], projects)}
