import hashlib
import sqlahelper
import sqlalchemy as sa
from pyramid.security import Everyone, Allow, Authenticated

class ShirlyResource(object):
    __acl__ = [
        (Allow, Authenticated, 'viewer'),
    ]
    def __init__(self, request):
        self.request = request


Base = sqlahelper.get_base()
DBSession = sqlahelper.get_session()

class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    user_name = sa.Column(sa.Unicode(255), unique=True)
    _password = sa.Column("password", sa.String(255))

    def set_password(self, password):
        self._password = hashlib.sha1(password).hexdigest()

    password = property(fset=set_password)

    def validate_password(self, password):
        return self._password == hashlib.sha1(password).hexdigest()
