import logging
from pyramid.view import view_config, view_defaults
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound
from .security import authenticate

@view_config(route_name='top', permission="viewer", renderer="shirly:templates/index.mak")
def index(request):
    logging.debug('%s' % request.environ['repoze.who.identity']['user'])
    return dict()

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
