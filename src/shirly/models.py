import hashlib
import sqlahelper
import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.sql as sql
from sqlalchemy.ext.associationproxy import association_proxy
from pyramid.security import Everyone, Allow, Authenticated

class ShirlyResource(object):
    __acl__ = [
        (Allow, Authenticated, 'viewer'),
    ]
    def __init__(self, request):
        self.request = request

    def query_users(self, in_=None):
        q = User.query
        if in_ is not None:
            q = q.filter(User.id.in_(in_))
        return q

    def query_project(self):
        return Project.query

    def add_project(self, project):
        return DBSession.add(project)

Base = sqlahelper.get_base()
DBSession = sqlahelper.get_session()

class User(Base):
    __tablename__ = 'users'
    query = DBSession.query_property()
    id = sa.Column(sa.Integer, primary_key=True)
    user_name = sa.Column(sa.Unicode(255), unique=True)
    _password = sa.Column("password", sa.String(255))

    def set_password(self, password):
        self._password = hashlib.sha1(password).hexdigest()

    password = property(fset=set_password)

    def validate_password(self, password):
        return self._password == hashlib.sha1(password).hexdigest()

    projects = association_proxy('members', 'project')

class Project(Base):
    __tablename__ = 'projects'
    query = DBSession.query_property()

    id = sa.Column(sa.Integer, primary_key=True)
    project_name = sa.Column(sa.Unicode(255), unique=True)
    description = sa.Column(sa.UnicodeText)

    users = association_proxy('members', 'user',
        creator=lambda user: Member(user=user))

class Member(Base):
    __tablename__ = 'members'
    id = sa.Column(sa.Integer, primary_key=True)
    project_id = sa.Column(sa.Integer, sa.ForeignKey('projects.id'))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))

    project = orm.relation('Project', backref='members')
    user = orm.relation('User', backref='members')

    @property
    def user_name(self):
        return self.user.user_name

