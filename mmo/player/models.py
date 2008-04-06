from django.db import models

from items.models import InventoryPile

XP_LIST = [250, 500, 1000] # @@@

class Player(models.Model):
    
    name = models.CharField(max_length=20)
    
    location = models.ForeignKey('map.Location')
    
    xp = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    
    energy = models.IntegerField(default=5000)
    mood = models.IntegerField(default=200)
    karma = models.IntegerField(default=200)
    
    def level(self):
        for level, xp in enumerate(XP_LIST):
            if self.xp < xp:
                return str(level + 1)
        return str(len(XP_LIST) + 1) + "+"
    
    def next_level_at(self):
        for xp in XP_LIST:
            if self.xp < xp:
                return str(xp)
        return "tbd"
    
    def inventory(self):
        return InventoryPile.objects.filter(player=self)
    
    def add_to_inventory(self, item_type, quantity):
        pile, created = InventoryPile.objects.get_or_create(item_type=item_type, player=self, defaults={'quantity': 0})
        pile.increase(quantity)
        return pile.quantity
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass