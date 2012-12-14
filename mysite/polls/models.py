"""
Polls are owned by users and have choices. Voting is indicated by
the choice.num_votes field.
"""
import datetime

from django.db import models
from django.contrib.auth.models import User

class SocialUser(models.Model):
    user = models.OneToOneField(User)
    twitter = models.CharField(max_length=200)
    facebook = models.CharField(max_length=200)
    g_plus = models.CharField(max_length=200)

    def __unicode__(self):
        return self.user.username


class Poll(models.Model):
    """
    A Poll, owned by a user, with associated choices.
    """
    user = models.ForeignKey(User)
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    @models.permalink
    def get_absolute_url(self):
        return ('poll_detail', [self.id])

    def was_published_recently(self):
        return self.pub_date.date() == datetime.date.today()

    def __unicode__(self):
        return self.question

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()

    def __unicode__(self):
        return self.choice
