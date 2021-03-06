import logging
from pyramid.view import view_config, view_defaults
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound
from pyramid_simpleform import Form
from js.tinymce import tinymce
from js.jquery import jquery
from js.jqueryui import jqueryui
from js.bootstrap import bootstrap
from .security import authenticate
from . import schemas as s
from . import models as m
from .forms import FormRenderer
from . import helpers as h

@view_config(route_name='top', permission="viewer", renderer="shirly:templates/index.mak")
def index(request):
    user = request.authenticated_user
    projects = user.projects
    return dict(projects=[dict(
            id=p.id,
            project_name=p.project_name,
        ) for p in projects])

@view_config(route_name="logout")
def logout(request):
    redirect = HTTPFound(location=request.route_url('top'))
    headers = forget(request)
    redirect.headerlist.extend(headers)
    return redirect


class LoginView(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name='login', request_method="GET", renderer='shirly:templates/login.mak')
    @view_config(context='pyramid.httpexceptions.HTTPForbidden', request_method="GET", renderer='shirly:templates/login.mak')
    def login_form(self):
        return dict()

    @view_config(route_name='login', request_method="POST", renderer='shirly:templates/login.mak')
    def login(self):
        logging.debug('login')
        identity = authenticate(self.request)
        if identity:
            headers = remember(self.request, identity)
            redirect = HTTPFound(location=self.request.route_url('top'))
            redirect.headerlist.extend(headers)
            return redirect

        logging.debug('login failed')
        
        return dict()

@view_defaults(permission="viewer")
class ProjectView(object):
    def __init__(self, request):
        self.request = request
        self.context = request.context

    @view_config(route_name="projects", renderer="shirly:templates/projects.mak", request_method="GET")
    def collection_get(self):
        projects = self.context.query_project().all()
        #return dict(projects=[dict(id=project.id, project_name=project.project_name, description=project.description)
        #    for project in projects])
        return dict(projects=projects)

    @view_config(route_name="project", renderer="shirly:templates/project.mak", request_method="GET")
    def member_get(self):
        project_name = self.request.matchdict['project_name']
        project = self.context.query_project().filter_by(project_name=project_name).one()
        return dict(id=project.id,
            project_name=project.project_name,
            description=project.description,
            members=[dict(id=u.id, user_name=u.user_name) 
                for u in project.users.values()],
            tickets=[dict(ticket_no=t.ticket_no, ticket_name=t.ticket_name) 
                for t in project.tickets.values()])

@view_defaults(permission="viewer")
class TicketView(object):
    def __init__(self, request):
        self.request = request
        self.context = request.context
        jquery.need()
        jqueryui.need()
        tinymce.need()

    @view_config(route_name="project_tickets", renderer="shirly:templates/tickets.mak")
    def collection_get(self):
        project = self.context.project
        tickets = sorted(project.tickets.values(), key=lambda t: t.ticket_no)
        logging.debug(project.tickets)
        return dict(project=project, tickets=tickets)

    @view_config(route_name="project_ticket", request_method="GET", renderer="shirly:templates/ticket.mak")
    def member_get(self):
        project = self.context.project
        t = self.context.ticket
        form = Form(self.request, schema=s.TicketSchema, obj=t)

        return dict(renderer=FormRenderer(form),
            project_name=project.project_name,
            ticket=t,
            members=[(u.id, u.user_name) for u in project.users.values()],
            ticket_no=t.ticket_no,
            ticket_name=t.ticket_name,
            reporter_name=t.reporter_name,
            status=t.status,
            owner_name=t.owner_name,
            description=t.description,
            reporter=t.reporter)


    @view_config(route_name="project_ticket", request_method="POST", request_param="update=Update")
    def update_ticket(self):
        project = self.context.project
        ticket = self.context.ticket
        form = Form(self.request, schema=s.TicketSchema, obj=ticket)
        if form.validate():
            form.bind(ticket)
            return HTTPFound(location=h.ticket_url(self.request, ticket))
    @view_config(route_name="project_ticket", request_method="POST", request_param="operation=Reopen")
    def reopen_ticket(self):
        t = self.context.ticket
        t.reopen()
        return HTTPFound(location=self.request.url)

    @view_config(route_name="project_ticket", request_method="POST", request_param="operation=Finish")
    def finish_ticket(self):
        t = self.context.ticket
        t.finish()
        return HTTPFound(location=self.request.url)

    @view_config(route_name="project_ticket", request_method="POST", request_param="operation=Close")
    def close_ticket(self):
        t = self.context.ticket
        t.close()
        return HTTPFound(location=self.request.url)

    @view_config(route_name="project_ticket", request_method="POST", request_param="operation=Assign")
    def assign_ticket(self):
        project = self.context.project
        owner_id = int(self.request.params['owner'])
        member = project.members[owner_id]
        t = self.context.ticket
        t.assign(member)
        return HTTPFound(location=self.request.url)

    @view_config(route_name="project_ticket", request_method="POST", request_param="operation=Accept")
    def accept_ticket(self):
        t = self.context.ticket
        t.accept()
        return HTTPFound(location=self.request.url)

@view_defaults(permission="viewer")
class TicketFormView(object):
    def __init__(self, request):
        self.request = request
        self.context = self.request.context
        jquery.need()
        jqueryui.need()
        tinymce.need()

    @view_config(route_name='project_new_ticket', request_method="GET", renderer="shirly:templates/new_ticket.mak")
    def get(self):
        project = self.context.project

        form = Form(self.request, schema=s.NewTicketSchema)
        members = [dict(id=m.id, user_name=m.user_name) for m in project.users.values()]
        return dict(renderer=FormRenderer(form),
            project_name=project.project_name,
            project_id=project.id,
            members=members)


    @view_config(route_name='project_new_ticket', request_method="POST", renderer="shirly:templates/new_ticket.mak")
    def post(self):
        project = self.context.project
        form = Form(self.request, schema=s.NewTicketSchema)
        if form.validate():
            ticket = form.bind(m.Ticket())
            ticket.reporter = self.context.member
            project.add_ticket(ticket)
            return HTTPFound(location=self.request.route_url('project_ticket', project_name=project.project_name, ticket_no=ticket.ticket_no))
        members = [dict(id=u.id, user_name=u.user_name) for u in project.users]
        return dict(renderer=FormRenderer(form),
            project_name=project.project_name,
            project_id=project.id,
            members=members)

@view_defaults(permission="viewer")
class ProjectFormView(object):
    def __init__(self, request):
        self.request = request
        self.context = request.context
        jquery.need()
        jqueryui.need()
        tinymce.need()

    @view_config(route_name='new_project', renderer='shirly:templates/new_project.mak', request_method="GET")
    def get(self):
        form = Form(self.request, schema=s.NewProjectSchema)
        users = self.context.query_users().all()
        return dict(renderer=FormRenderer(form),
            users=[(u.id, u.user_name) for u in users])

    @view_config(route_name='new_project', renderer='shirly:templates/new_project.mak', request_method="POST")
    def post(self):
        form = Form(self.request, schema=s.NewProjectSchema)
        if form.validate():
            project = form.bind(m.Project())
            users = self.context.query_users(in_=self.request.POST.getall('member'))
            for u in users:
                project.members[u.id] = m.Member(user=u)
            self.context.add_project(project)
            return HTTPFound('/')
        users = self.conext.query_users().all()
        return dict(renderer=FormRenderer(form),
            users=[(u.id, u.user_name) for u in users])

@view_defaults(permission="viewer")
class MilestoneView(object):
    def __init__(self, request):
        self.request = request
        self.context = self.request.context

    @view_config(route_name='project_milestones', renderer='shirly:templates/milestones.mak', request_method="GET")
    def collection_get(self):
        project = self.context.project
        milestones = project.milestones
        return dict(project_name=project.project_name,
            milestones=[
                dict(id=m.id, milestone_name=m.milestone_name, description=m.description, due_date=m.due_date,
                    ticket_count=len(m.tickets))
                for m in milestones
            ])

@view_defaults(permission="viewer")
class MilestoneFormView(object):
    def __init__(self, request):
        self.request = request
        self.context = self.request.context
        jquery.need()
        jqueryui.need()
        tinymce.need()

    @view_config(route_name='project_new_milestone', request_method="GET", renderer="shirly:templates/new_milestone.mak")
    def get(self):
        project = self.context.project

        form = Form(self.request, schema=s.NewMilestoneSchema)
        return dict(renderer=FormRenderer(form),
            project_name=project.project_name,
            project_id=project.id)


    @view_config(route_name='project_new_milestone', request_method="POST", renderer="shirly:templates/new_milestone.mak")
    def post(self):
        project = self.context.project
        form = Form(self.request, schema=s.NewMilestoneSchema)
        if form.validate():
            milestone = form.bind(m.Milestone())
            project.add_milestone(milestone)
            return HTTPFound(location=self.request.route_url('project_milestones', project_name=project.project_name))
        return dict(renderer=FormRenderer(form),
            project_name=project.project_name,
            project_id=project.id,
            )
