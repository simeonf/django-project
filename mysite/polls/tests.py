"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import Group
from polls.forms import VoteForm

class SimpleTest(TestCase):
    def setUp(self):
        Group(name="poll_users").save()

    def tearDown(self):
        Group.objects.all().delete()
    
    def test_choice_form_required(self):
        """
        Tests that my choice form requires a choice
        """
        form = VoteForm({})
        self.assertFalse(form.is_valid())
        self.assertIn('choice', form.errors)
        self.assertIn('required', "\n".join(form.errors.get('choice')))

    def test_group_exists(self):
        self.assertTrue(Group.objects.filter(name="poll_users"))

class ThrowawayTest(TestCase):

    def test_should_fail(self):
        self.assertTrue(False)
        
