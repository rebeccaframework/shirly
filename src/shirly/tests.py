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
