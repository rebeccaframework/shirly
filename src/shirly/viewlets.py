from pyramid.view import view_config

@view_config(context='.models.ShirlyResource', name="member_list", renderer="shirly:templates/viewlets/member_list.mak")
def memeber_list(request):
    project = request.context.project
    return dict(members=[
        dict(id=u.id, user_name=u.user_name)
        for u in project.users
        ])


@view_config(context='.models.ShirlyResource', name="ticket_list", renderer="shirly:templates/viewlets/ticket_list.mak")
def projects(request):
    project = request.context.project
    return dict(tickets=[
        dict(id=t.id, ticket_no=t.ticket_no, ticket_name=t.ticket_name)
        for t in project.tickets.values()
        ], 
        project_name=project.project_name)
