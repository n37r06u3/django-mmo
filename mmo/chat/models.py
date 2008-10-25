from django.db import models
import datetime
from mmo.player.models import Player

# Create your models here.
class GenericMessage(models.Model):
    """ Abstract Message which represents a message and a timestamp """
    message = models.CharField(blank=False, max_length=255)
    timestamp = models.DateTimeField(blank=True, default=datetime.datetime.now())
    
    class Meta:
        abstract = True
        ordering = ['-timestamp']

class ChatMessage(GenericMessage):
    """ Global Chat Message """
    from_player = models.ForeignKey(Player)
    
    def __unicode__(self):
        return "(%s) %s: %s" % (self.timestamp, self.from_player.name, self.message)

class PrivateMessage(GenericMessage):
    """ 
    Chat Message from one person to another 
    Not in the original GNE
    """
    from_player = models.ForeignKey(Player, related_name="from")
    to_player = models.ForeignKey(Player, related_name="to")
    
    def __unicode__(self):
        return "PRIVATE: (%s) %s -> %s: %s" % (self.timestamp, self.from_player.name, self.to_player.name, self.message)

class ServerMessage(GenericMessage):
    """ Message from server to a specific player """
    to_player = models.ForeignKey(Player)
    
    def __unicode__(self):
        return "SERVER: (%s) %s: %s" % (self.timestamp, self.to_player.name, self.message)
    