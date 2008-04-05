from django.db import models

from items.models import InventoryPile

class Player(models.Model):
    
    name = models.CharField(max_length=20)
    
    location = models.ForeignKey('map.Location')
    
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