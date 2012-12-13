"""
Integration tests using the testclient. Run separately from the unit tests...
"""
from datetime import datetime as dt
from django.contrib.auth.models import User
from django.test import TestCase

from polls.models import Poll, Choice

class SmokeTests(TestCase):
    @classmethod
    def setUpClass(cls):
        u = User.objects.create_user('simeon', 'simeonf@gmail.com', 'password')
        p = Poll(user=u, question="Why?", pub_date=dt.now())
        p.save()
        Choice.objects.bulk_create([Choice(poll=p, choice="Because", votes=0),
                                    Choice(poll=p, choice="Because", votes=0)])
        cls.p = p
        
    def test_polls_index(self):
        """
        Test that the polls index page comes up, has a login link, has
        a list of polls
        
        """
        resp = self.client.get("/polls/") # should be reversed, right?
        self.assertIn("Login", resp.content)
        self.assertIn(SmokeTests.p.get_absolute_url(), resp.content) 
        
