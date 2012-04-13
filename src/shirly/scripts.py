import sys
from pyramid.paster import bootstrap
import sqlahelper
from . import models as m

def add_user():
    env = bootstrap(sys.argv[1])
    settings = env['registry'].settings

    user_name = raw_input('user name: ')
    password = raw_input('password: ')
    user = m.User(user_name=user_name, password=password)
    m.DBSession.add(user)
    import transaction
    transaction.commit()
