from django.db import models

from datetime import datetime

# @@@ GNE also looks like it had unique items, which aren't covered here yet

class ItemType(models.Model):
    
    name = models.CharField(max_length=30)
    description = models.TextField()
    
    # @@@ icon
    # @@@ weight
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass


class InventoryPile(models.Model): # @@@ longing for model inheritance
    """
    a pile of a particular type of item in a player's inventory.
    """
    
    item_type = models.ForeignKey(ItemType)
    quantity = models.PositiveIntegerField()
    
    player = models.ForeignKey('player.Player')
    
    def drop_list(self):
        # utility method for enumerating possible quantities that can be dropped from this pile
        return [quantity for quantity in [1, 2, 5, 10, 25, 50, 100] if quantity < self.quantity] + [self.quantity]
    
    def reduce(self, quantity):
        q = min(self.quantity, quantity)
        self.quantity -= q
        self.save()
        if self.quantity == 0:
            self.delete()
        return q
    
    def increase(self, quantity):
        self.quantity += quantity
        self.save()
        return self.quantity
    
    class Meta:
        unique_together = (
            ('item_type', 'player'),
        )
    
    def __unicode__(self):
        return u"%s has %s [%s]" % (self.player, self.item_type, self.quantity)
    
    class Admin:
        pass


class LocationPile(models.Model): # @@@ longing for model inheritance
    """
    a pile of a particular type of item in a location.
    """
    
    item_type = models.ForeignKey(ItemType)
    quantity = models.PositiveIntegerField() # if a generator pile this is in addition to what's been generated
    
    # for generator piles
    start_time = models.DateTimeField(null=True, blank=True) # when to start generating from
    regen = models.PositiveIntegerField(null=True, blank=True) # how many seconds before a new item gets generated
    
    # @@@ in absence of model mixin, can't decide whether to use location object
    # @@@ or just duplicate code
    # location = models.ForeignKey('map.Location')
    # @@@ going with duplicate code for now
    hub = models.ForeignKey('map.Hub')
    lot = models.ForeignKey('map.Lot', null=True, blank=True) # must be a Lot in the self.hub Hub
    
    def total_quantity(self):
        if self.regen:
            delta = datetime.now() - self.start_time
            seconds = 86400 * delta.days + delta.seconds
            return (seconds / self.regen) + self.quantity
        else:
            return self.quantity
    
    def pickup_list(self):
        # utility method for enumerating possible quantities that can be picked up from this pile
        return [quantity for quantity in [1, 2, 5, 10, 25, 50, 100] if quantity < self.total_quantity()] + [self.total_quantity()]
    
    def reduce(self, quantity):
        q = min(self.total_quantity(), quantity)
        self.quantity -= q
        self.save()
        return q
    
    def increase(self, quantity):
        self.quantity += quantity
        self.save()
        return self.quantity
    
    def location_display(self):
        if self.lot:
            return u"%s in %s" % (self.lot.name, self.hub.name)
        else:
            return self.hub.name
    
    def __unicode__(self):
        if self.regen:
            return u"%s in %s every %s seconds (%s additional; now %s)" % (self.item_type, self.lot, self.regen, self.quantity, self.total_quantity())
        else:
            return u"%s [%s] in %s" % (self.item_type, self.total_quantity(), self.location_display())
        
    class Admin:
        pass
