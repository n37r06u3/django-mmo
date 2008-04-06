from django.db import models
import datetime
from mmo.player.models import Player

# Create your models here.
class Chat(models.Model):
	""" Chat Module """
	player = models.ForeignKey(Player)
	message = models.CharField(blank=False, max_length=255)
	timestamp = models.DateTimeField(blank=True, default=datetime.datetime.now())
	

	class Admin:
		pass

	def __unicode__(self):
		return "(%s) %s: %s" % (self.timestamp, self.player.name, self.message)
