import logging
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid_who.whov2 import WhoV2AuthenticationPolicy
from repoze.who.api import get_api as get_who_api
from repoze.who.interfaces import IAPIFactory

def includeme(config):
    who_ini = config.registry.settings['who.ini']
    authorization_policy = ACLAuthorizationPolicy()
    authentication_policy = WhoV2AuthenticationPolicy(who_ini,
        identifier_id='auth_tkt')
    api_factory = authentication_policy._api_factory
    config.registry.registerUtility(api_factory, IAPIFactory)
    config.set_authorization_policy(authorization_policy)
    config.set_authentication_policy(authentication_policy)

    config.add_tween('shirly.security.who_api_tween_factory')

    config.set_request_property(authenticated_user, 'authenticated_user')

def who_api_tween_factory(handler, registry):
    api_factory = registry.getUtility(IAPIFactory)
    def who_api_tween(request):
        api_factory(request.environ)
        return handler(request)
    return who_api_tween

def authenticate(request):
    who_api = get_who_api(request.environ)
    identity, headers = who_api.login({'login': request.params['login'], 'password': request.params['password']})
    return identity.get('repoze.who.userid')

def authenticated_user(request):
    return request.environ.get('repoze.who.identity', {}).get('user')
