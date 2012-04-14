#
from pyramid.config import Configurator
import sqlahelper
from sqlalchemy import engine_from_config
from . import helpers as h

def add_renderer_globals(event):
    event['h'] = h

def main(global_config, **settings):
    engine = engine_from_config(settings)
    sqlahelper.add_engine(engine)
    config = Configurator(settings=settings,
        root_factory='.models.ShirlyResource')
    config.add_route('top', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('projects', '/projects')
    config.add_route('new_project', '/projects;new')
    config.add_route('project', '/projects/{project_name}')
    config.add_route('project_tickets', '/projects/{project_name}/tickets')
    config.add_route('project_new_ticket', '/projects/{project_name}/tickets;new')
    config.add_route('project_ticket', '/projects/{project_name}/tickets/{ticket_no}')
    config.add_subscriber(add_renderer_globals, 'pyramid.events.BeforeRender')
    config.scan()
    return config.make_wsgi_app()
