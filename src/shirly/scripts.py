import sys
import locale
import getpass
from pyramid.paster import bootstrap
import sqlahelper
from . import models as m

def add_user():
    env = bootstrap(sys.argv[1])
    settings = env['registry'].settings

    user_name = unicode(raw_input('user name: '), locale.getpreferredencoding())
    password = getpass.getpass('password: ')
    user = m.User(user_name=user_name, password=password)
    m.DBSession.add(user)
    import transaction
    transaction.commit()
