from webhelpers.html.builder import *
from webhelpers.html.tags import *
from pyramid.view import render_view_to_response

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

def member_list(request):
    res = render_view_to_response(request.context, request, name='member_list')
    return res.text

def ticket_list(request):
    res = render_view_to_response(request.context, request, name='ticket_list')
    return res.text
    
def milestone_list(request):
    res = render_view_to_response(request.context, request, name='milestone_list')
    return res.text
