from django.db import models
from mmo.player.models import Player
import datetime

# Create your models here.
class Note(models.Model):
    """ This will hold private notes for each player"""
    notes = models.TextField(blank=True)
    player = models.ForeignKey(Player)
    last_updated = models.DateTimeField(blank=True, default=datetime.datetime.now())

    def __unicode__(self):
        return "%s's notes" % self.player.name
