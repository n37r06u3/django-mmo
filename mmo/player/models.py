from django.db import models

from items.models import *

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
    
    def make_list(self):
        # what can I make?
        
        # prefetch inventory counts
        item_counts = {}
        for pile in self.inventory():
            item_counts[pile.item_type.id] = pile.quantity
        
        targets = []
        
        for target in MakeTarget.objects.all():
            missing = False
            for ingredient in target.makeingredient_set.all():
                if item_counts.get(ingredient.item_type.id, 0) < ingredient.quantity:
                    missing = True
                    break
            if not missing:
                targets.append(target)
        
        return targets
    
    def make(self, target):
        for ingredient in target.makeingredient_set.all():
            pile = InventoryPile.objects.get(item_type=ingredient.item_type, player=self)
            pile.reduce(ingredient.quantity)
        self.add_to_inventory(target.item_type, target.quantity)
    
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

    player = models.ForeignKey(Player)

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
