#
from pyramid.config import Configurator
import sqlahelper
from sqlalchemy import engine_from_config

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
    config.scan()
    return config.make_wsgi_app()
