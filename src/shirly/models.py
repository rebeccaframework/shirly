import hashlib
import sqlahelper
import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.sql as sql
from sqlalchemy.orm.collections import attribute_mapped_collection
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
    ticket_counter = sa.Column(sa.Integer, default=0)

    users = association_proxy('members', 'user',
        creator=lambda user: Member(user=user))

    tickets = orm.relation('Ticket', backref='project', collection_class=attribute_mapped_collection('ticket_no'))

    def gen_ticket_no(self):
        self.ticket_counter += 1
        return self.ticket_counter

    def add_ticket(self, ticket):
        ticket.ticket_no = self.gen_ticket_no()
        self.tickets[ticket.ticket_no] = ticket
        return ticket

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

class Ticket(Base):
    __tablename__ = 'tickets'
    id = sa.Column(sa.Integer, primary_key=True)
    project_id = sa.Column(sa.Integer, sa.ForeignKey('projects.id'))
    member_id = sa.Column(sa.Integer, sa.ForeignKey('members.id'))

    user = orm.relation('Member', backref='tickets')

    ticket_no = sa.Column(sa.Integer)
    ticket_name = sa.Column(sa.Unicode(255))
    description = sa.Column(sa.UnicodeText)
    estimated_time = sa.Column(sa.Integer)
