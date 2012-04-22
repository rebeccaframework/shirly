import unittest
from pyramid import testing

def _setup_db():
    import sqlahelper
    from sqlalchemy import create_engine
    sqlahelper.add_engine(create_engine("sqlite:///"))
    from . import models as m
    m.Base.metadata.create_all()

def _teardown_db():
    import transaction
    transaction.abort()
    import sqlahelper
    sqlahelper.get_session().remove()
    from . import models as m
    m.Base.metadata.drop_all()

def setUp():
    _setup_db()

def tearDown():
    _teardown_db()

class ShirlyResourceTests(unittest.TestCase):
    def tearDown(self):
        import transaction
        transaction.abort()

    def _getTarget(self):
        from .models import ShirlyResource
        return ShirlyResource

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_project_without_matchdict(self):
        request = testing.DummyRequest(matchdict={})
        target = self._makeOne(request)

        self.assertIsNone(target.project)

    def test_project_without_project(self):
        request = testing.DummyRequest(matchdict={'project_name': u'test-project'})
        target = self._makeOne(request)

        self.assertIsNone(target.project)

    def test_project(self):
        from . import models as m
        p = m.Project(project_name=u"test-project")
        m.DBSession.add(p)
        m.DBSession.flush()
        request = testing.DummyRequest(matchdict={'project_name': u'test-project'})
        target = self._makeOne(request)

        self.assertEqual(target.project, p)

    def test_add_project(self):
        from . import models as m
        p = m.Project(project_name=u"test-project")
        request = testing.DummyRequest()
        target = self._makeOne(request)
        target.add_project(p)

        p2 = m.Project.query.filter(m.Project.project_name==u"test-project").one()
        self.assertEqual(p2, p)


    def test_ticket_no_without_matchdict(self):
        request = testing.DummyRequest(matchdict={})
        target = self._makeOne(request)
        
        self.assertIsNone(target.ticket_no)

    def test_ticket_no(self):
        request = testing.DummyRequest(matchdict={'ticket_no': '10'})
        target = self._makeOne(request)
        
        self.assertEqual(target.ticket_no, 10)

    def test_ticket_without_project(self):
        request = testing.DummyRequest(matchdict={'ticket_no': '10'})
        target = self._makeOne(request)
        target.project = None
        
        self.assertIsNone(target.ticket)

    def test_ticket_without_ticket_no(self):
        class DummyProject(object):
            def __init__(self):
                self.called = []
            def get_ticket(self, ticket_no):
                self.called.append(ticket_no)

        request = testing.DummyRequest(matchdict={})
        target = self._makeOne(request)
        project = DummyProject()
        target.project = project
        
        self.assertIsNone(target.ticket)
        self.assertEqual(project.called, [None])

    def test_ticket(self):
        ticket_marker = object()
        class DummyProject(object):
            def __init__(self):
                self.called = []
            def get_ticket(self, ticket_no):
                self.called.append(ticket_no)
                return ticket_marker

        request = testing.DummyRequest(matchdict={'ticket_no': '10'})
        target = self._makeOne(request)
        project = DummyProject()
        target.project = project
        
        self.assertEqual(target.ticket, ticket_marker)

    def test_member_without_project(self):
        request = testing.DummyRequest(matchdict={'ticket_no': '10'})
        target = self._makeOne(request)

        self.assertIsNone(target.member)

    def test_member_without_authenticated_user(self):
        from . import models as m
        p = m.Project(project_name=u"test-project")
        request = testing.DummyRequest(matchdict={'ticket_no': '10'},
            authenticated_user=None)
        target = self._makeOne(request)
        target.project = p

        self.assertIsNone(target.member)

    def test_member(self):
        import sqlahelper
        from . import models as m
        p = m.Project(project_name=u"test-project")
        u = m.User(user_name=u'test-user')
        m = m.Member(project=p, user=u)
        sqlahelper.get_session().add(m)
        request = testing.DummyRequest(matchdict={'ticket_no': '10'},
            authenticated_user=u)
        target = self._makeOne(request)
        target.project = p

        self.assertEqual(target.member, m)

class ProjectTests(unittest.TestCase):

    def _getTarget(self):
        from .models import Project
        return Project

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_add_ticket(self):

        from .models import Ticket
        ticket = Ticket()

        target = self._makeOne(ticket_counter=0)
        ticket = target.add_ticket(ticket)

        self.assertEqual(ticket.ticket_no, 1)
        self.assertEqual(target.tickets[ticket.ticket_no], ticket)
        self.assertEqual(target.ticket_counter, 1)

    def test_add_milestone(self):

        from .models import Milestone
        milestone = Milestone()

        target = self._makeOne()
        target.add_milestone(milestone)

        self.assertIn(milestone, target.milestones)

    def test_get_ticket(self):

        from .models import Ticket
        ticket = Ticket(ticket_no=10)

        target = self._makeOne(ticket_counter=0)
        target.tickets[ticket.ticket_no] = ticket

        result = target.get_ticket(10)
        self.assertEqual(result, ticket)

    def test_ticket_count_empty(self):
        target = self._makeOne()
        self.assertEqual(target.ticket_count, 0)

    def test_ticket_count(self):
        from .models import Ticket
        ticket = Ticket()
        target = self._makeOne()
        target.tickets[ticket.ticket_no] = ticket
        self.assertEqual(target.ticket_count, 1)

    def test_active_ticket_count_empty(self):
        target = self._makeOne()
        self.assertEqual(target.active_ticket_count, 0)

    def test_active_ticket_count(self):
        from .import models as m
        target = self._makeOne()
        for status in ('new', 'assigned', 'accepted', 'finished', 'closed'):
            t = m.Ticket(status=status, project=target)
            m.DBSession.add(t)
        m.DBSession.flush()
        self.assertEqual(target.active_ticket_count, 4)

class TicketTests(unittest.TestCase):

    def _getTarget(self):
        from .models import Ticket
        return Ticket

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_reporter_name(self):
        from . import models as m
        target = self._makeOne(reporter=m.Member(user=m.User(user_name=u'ticket-reporter')))

        self.assertEqual(target.reporter_name, u'ticket-reporter')

    def test_reporter_name_without_reporter(self):
        target = self._makeOne()

        self.assertIsNone(target.reporter_name)

    def test_owner_name(self):
        from . import models as m
        target = self._makeOne(owner=m.Member(user=m.User(user_name=u'ticket-owner')))

        self.assertEqual(target.owner_name, u'ticket-owner')

    def test_owner_name_without_owner(self):
        target = self._makeOne()

        self.assertIsNone(target.owner_name)

    def test_reopen(self):
        target = self._makeOne()
        target.reopen()
        self.assertEqual(target.status, "new")

    def test_assign(self):
        from . import models as m
        target = self._makeOne()
        member = m.Member(user=m.User(user_name=u'ticket-owner'))

        target.assign(member)

        self.assertEqual(target.status, "assigned")
        self.assertEqual(target.owner, member)

    def test_accept(self):
        target = self._makeOne()
        target.accept()
        self.assertEqual(target.status, "accepted")

    def test_finish(self):
        target = self._makeOne()
        target.finish()
        self.assertEqual(target.status, "finished")

    def test_is_finished_instance_unfinished(self):
        target = self._makeOne()
        self.assertFalse(target.is_finished)

    def test_is_finished_instance(self):
        target = self._makeOne(status="finished")
        self.assertTrue(target.is_finished)

    def test_is_finished_class(self):
        import operator
        target = self._getTarget()
        result = target.is_finished

        self.assertEqual(result.operator, operator.eq)
        self.assertEqual(result.left, target.status)
        self.assertEqual(result.right.value, "finished")

    def test_close(self):
        target = self._makeOne()

        target.close()

        self.assertEqual(target.status, "closed")

    def test_is_closed_instance_unclosed(self):
        target = self._makeOne()

        self.assertFalse(target.is_closed)

    def test_is_closed_instance(self):
        target = self._makeOne(status="closed")

        self.assertTrue(target.is_closed)

    def test_is_closed_class(self):
        import operator
        target = self._getTarget()
        result = target.is_closed

        self.assertEqual(result.operator, operator.eq)
        self.assertEqual(result.left, target.status)
        self.assertEqual(result.right.value, "closed")

    def test_is_active_instance_closed(self):
        target = self._makeOne(status="closed")

        self.assertFalse(target.is_active)

    def test_is_active_instance_unclosed(self):
        target = self._makeOne(status="new")

        self.assertTrue(target.is_active)

    def test_is_active_class(self):
        import operator
        target = self._getTarget()
        result = target.is_active

        self.assertEqual(result.operator, operator.ne)
        self.assertEqual(result.left, target.status)
        self.assertEqual(result.right.value, "closed")

    def test_join_to_instance(self):
        from . import models as m
        p = m.Project()
        target = self._makeOne(project=p)

        self.assertTrue(target.join_to(p))

    def test_join_to_class(self):
        import operator
        from . import models as m
        p = m.Project()
        p.id = 1
        target = self._getTarget()
        result = target.join_to(p)

        self.assertEqual(result.operator, operator.eq)
        self.assertEqual(result.left.effective_value, 1)
        self.assertEqual(result.right, target.project_id)

class UserTests(unittest.TestCase):
    def tearDown(self):
        import transaction
        transaction.abort()

    def _getTarget(self):
        from .models import User
        return User

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_set_password(self):
        target = self._makeOne()
        target.set_password('secret')

        self.assertIsNotNone(target._password)
        self.assertNotEqual(target._password, 'secret')

    def test_validate_password(self):
        target = self._makeOne()
        target.set_password('secret')

        self.assertTrue(target.validate_password('secret'))

    def test_owned_tickets_empty(self):
        target = self._makeOne()
        self.assertEqual(target.owned_tickets, [])

    def test_owned_tickets(self):
        from . import models as m
        target = self._makeOne()
        p = m.Project(project_name=u"test-project")
        member = m.Member(project=p, user=target)
        t = m.Ticket(owner=member)
        m.DBSession.add(t)
        m.DBSession.flush()

        self.assertEqual(target.owned_tickets[0], t)

    def test_reported_tickets_empty(self):
        target = self._makeOne()
        self.assertEqual(target.reported_tickets, [])

    def test_reported_tickets(self):
        from . import models as m
        target = self._makeOne()
        p = m.Project(project_name=u"test-project")
        member = m.Member(project=p, user=target)
        t = m.Ticket(reporter=member)
        m.DBSession.add(t)
        m.DBSession.flush()

        self.assertEqual(target.reported_tickets[0], t)

class MemberTests(unittest.TestCase):
    def tearDown(self):
        import transaction
        transaction.commit()

    def _getTarget(self):
        from .models import Member
        return Member

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)


    def test_by_user_id(self):
        from . import models as m
        u = m.User()
        member = self._makeOne(user=u)
        m.DBSession.add(member)
        m.DBSession.flush()

        target = self._getTarget()
        result = target.by_user_id(u.id)

        self.assertEqual(result, member)



class ProjectUrlTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('shirly')

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, *args, **kwargs):
        from .helpers import project_url
        return project_url(*args, **kwargs)

    def test_it(self):
        project = testing.DummyResource(project_name=u'test-project')
        request = testing.DummyRequest()
        result = self._callFUT(request, project)

        self.assertEqual(result, 'http://example.com/projects/test-project')

class LinkToProjectTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('shirly')

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, *args, **kwargs):
        from .helpers import link_to_project
        return link_to_project(*args, **kwargs)

    def test_it(self):
        from webhelpers.html.builder import literal
        project = testing.DummyResource(project_name=u'test-project')
        request = testing.DummyRequest()
        result = self._callFUT(request, project)

        self.assertEqual(result, literal(u'<a href="http://example.com/projects/test-project">test-project</a>'))

class TicketUrlTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('shirly')

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, *args, **kwargs):
        from .helpers import ticket_url
        return ticket_url(*args, **kwargs)

    def test_it(self):
        project = testing.DummyResource(project_name=u'test-project')
        ticket = testing.DummyResource(project=project, ticket_no=999)
        request = testing.DummyRequest()
        result = self._callFUT(request, ticket)

        self.assertEqual(result, 'http://example.com/projects/test-project/tickets/999')

class LinkToTicketTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('shirly')

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, *args, **kwargs):
        from .helpers import link_to_ticket
        return link_to_ticket(*args, **kwargs)

    def test_it(self):
        from webhelpers.html.builder import literal
        project = testing.DummyResource(project_name=u'test-project')
        ticket = testing.DummyResource(project=project, ticket_no=999, ticket_name=u'test-ticket')
        request = testing.DummyRequest()
        result = self._callFUT(request, ticket)

        self.assertEqual(result, literal(u'<a href="http://example.com/projects/test-project/tickets/999">test-ticket</a>'))

class BreadCrumbTests(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from .helpers import breadcrumb
        return breadcrumb(*args, **kwargs)

    def test_empty(self):
        result = self._callFUT([])
        self.assertEqual(result, "")

    def test_one(self):
        from webhelpers.html.builder import literal
        result = self._callFUT(["HOME"])
        self.assertEqual(result, literal(u'<ul class="breadcrumb"><li class="active">HOME</li></ul>'))

    def test_many(self):
        from webhelpers.html.builder import literal
        result = self._callFUT([("/", "HOME"), "Projects"])
        self.assertEqual(result, literal(u'<ul class="breadcrumb">'
            '<li><a href="/">HOME</a><span class="divider">/</span></li>'
            '<li class="active">Projects</li>'
            '</ul>'))

class GridTests(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from .helpers import grid
        return grid(*args, **kwargs)

    def test_it(self):
        from webhelpers.html.builder import literal
        request = testing.DummyRequest()
        data = [testing.DummyResource(name="dummy %d" % i, v1=i*2, v2=i+1) for i in range(2)]
        result = self._callFUT(request, [('Name', 'name'), ('Sum', lambda o: o.v1 + o.v2)], data)

        self.assertEqual(result, literal(u'<table class="table"> '
            '<thead><tr><th>Name</th><th>Sum</th></tr></thead>'
            '<tbody>'
            '<tr><td>dummy 0</td><td>1</td></tr>'
            '<tr><td>dummy 1</td><td>4</td></tr>'
            '</tbody>'
            '</table>'))

class RenderViewletTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, *args, **kwargs):
        from .helpers import render_viewlet
        return render_viewlet(*args, **kwargs)

    def test_it(self):
        from pyramid.response import Response
        from .models import ShirlyResource
        def dummy_view(request):
            request.response.text = u'OK'
            return request.response

        self.config.add_view(dummy_view, context=ShirlyResource, name="dummy-viewlet")
        request = testing.DummyRequest(response=Response(), registry=self.config.registry)
        resource = ShirlyResource(request)
        request.context = resource
        
        result = self._callFUT(request, "dummy-viewlet")
        self.assertEqual(result, u'OK')

