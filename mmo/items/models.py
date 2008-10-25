from django.db import models

from datetime import datetime

# @@@ GNE also looks like it had unique items, which aren't covered here yet

class ItemType(models.Model):
    """ Indicates an object that can be interacted with """
    
    name = models.CharField(max_length=30)
    description = models.TextField()
    
    icon_code = models.IntegerField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __unicode__(self):
        return self.name
    
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
            return u"%s in %s every %s seconds (%s additional; now %s)" % (self.item_type, self.location_display(), self.regen, self.quantity, self.total_quantity())
        else:
            return u"%s [%s] in %s" % (self.item_type, self.total_quantity(), self.location_display())
        
    class Admin:
        pass


class MakeTarget(models.Model):
    """ Represents something that can be created """
    quantity = models.PositiveIntegerField(default=1)
    item_type = models.ForeignKey(ItemType)
    
    # @@@ make skill
    
    def __unicode__(self):
        return u"%s x %s" % (self.quantity, self.item_type)
    
    class Admin:
        pass


class MakeIngredient(models.Model):
    """ Represents a combination of items that must be combined to make something """
    target = models.ForeignKey(MakeTarget)
    quantity = models.PositiveIntegerField(default=1)
    item_type = models.ForeignKey(ItemType)
    
    def __unicode__(self):
        return u"%s x %s for %s" % (self.quantity, self.item_type, self.target)
    
    class Admin:
        pass