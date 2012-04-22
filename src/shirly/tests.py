import unittest
from pyramid import testing

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
