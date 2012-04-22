from webhelpers.html.builder import *
from webhelpers.html.tags import *
from pyramid.view import render_view_to_response
from operator import itemgetter, attrgetter
from functools import partial

def breadcrumb(seq):
    if len(seq) == 0:
        return ""

    html = []
    html.append('<ul class="breadcrumb">')
    for url, label in seq[:-1]:
        html.append(
            ('<li>'
            '<a href="%(url)s">%(label)s</a>'
            '<span class="divider">/</span>'
            '</li>') % dict(url=url, label=label))
    html.append('<li class="active">%s</li>' % seq[-1])
    html.append('</ul>')
    return literal("".join(html))

def render_viewlet(request, name):
    res = render_view_to_response(request.context, request, name=name)
    return res.text

member_list = partial(render_viewlet, name="member_list")
ticket_list = partial(render_viewlet, name="ticket_list")
milestone_list = partial(render_viewlet, name="milestone_list")


def project_url(request, project):
    return request.route_url('project', project_name=project.project_name)

def link_to_project(request, project):
    return literal('<a href="%s">%s</a>' % (project_url(request, project), project.project_name))

def ticket_url(request, ticket):
    return request.route_url('project_ticket', project_name=ticket.project.project_name, ticket_no=ticket.ticket_no)

def link_to_ticket(request, ticket):
    return literal('<a href="%s">%s</a>' % (ticket_url(request, ticket), ticket.ticket_name))

def grid(request, columns, data):
    html = ['<table class="table"> ',
        '<thead>',
        '<tr>',
    ]

    for name, _ in columns:
        html.append('<th>%s</th>' % name)

    html.extend([
        '</tr>',
        '</thead>',
        '<tbody>',
    ])

    for d in data:
        html.append('<tr>')
        for _, col in columns:
            if callable(col):
                html.append('<td>%s</td>' % col(d))
            else:
                html.append('<td>%s</td>' % getattr(d, col))
        html.append('</tr>')

    html.extend([
        '</tbody>',
        '</table>',
    ])

    return literal(unicode("".join(html)))
