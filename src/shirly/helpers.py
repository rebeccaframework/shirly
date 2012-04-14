from webhelpers.html.builder import *
from webhelpers.html.tags import *
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
