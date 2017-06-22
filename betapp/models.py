from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django_mysql.models import JSONField, Model


class Player(Model):
    en_name = models.CharField(max_length=200)
    cn_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.cn_name


class Club(Model):
    en_club_name = models.CharField(max_length=200)
    cn_club_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.cn_club_name


class BetOdds(Model):
    t_created = models.DateTimeField(auto_now_add=True)
    odds = JSONField()
    club_rumors = JSONField()
