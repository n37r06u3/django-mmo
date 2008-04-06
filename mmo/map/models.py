from django.db import models

from items.models import LocationPile

class Hub(models.Model):
    
    name = models.CharField(max_length=30)
    description = models.TextField()
    
    # @@@ eventually this will have an x, y location for the visual map
    
    def roads(self):
        r = []
        for road in self.roads_one.all():
            r.append({"direction": road.direction_two_from_one, "destination": road.hub_two})
        for road in self.roads_two.all():
            r.append({"direction": road.direction_one_from_two(), "destination": road.hub_one})
        return r
    
    def lots(self):
        return self.lot_set.order_by('position')
    
    def who_is_here(self):
        players = set()
        for location in Location.objects.filter(hub=self, lot__isnull=True, visible=True):
            players = players.union(location.player_set.all())
        return len(players), players
    
    def what_is_here(self):
        return [pile for pile in LocationPile.objects.filter(hub=self, lot__isnull=True) if pile.total_quantity() > 0]
    
    def drop_here(self, item_type, quantity):
        pile, created = LocationPile.objects.get_or_create(item_type=item_type, hub=self, lot__isnull=True, defaults={'quantity': 0})
        return pile.increase(quantity)
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass


class Road(models.Model):
    
    # the west-most hub goes first, unless road is north-south in which case
    # the north-most hub goes first.
    
    hub_one = models.ForeignKey(Hub, related_name="roads_one")
    hub_two = models.ForeignKey(Hub, related_name="roads_two")
    
    # the direction of hub_two relative to hub_one, expresses as 16-point
    # compass direction. Because west-most hub goes first, only possible
    # choices here are: NNE, NE, ENE, E, ESE, SE, SSE, S
    direction_two_from_one = models.CharField(max_length=3)
    
    def direction_one_from_two(self):
        return {
            "NNE": "SSW",
            "NE": "SW",
            "ENE": "WSW",
            "E": "W",
            "ESE": "WNW",
            "SE": "NW",
            "SSE": "NNW",
            "S": "N",
        }[self.direction_two_from_one]
    
    def __unicode__(self):
        return "%s road from %s to %s" % (self.direction_two_from_one, self.hub_one, self.hub_two)
    
    class Admin:
        pass


class Lot(models.Model):
    
    hub = models.ForeignKey(Hub)
    
    # 0 thru 7
    position = models.IntegerField(choices = [(i, str(i)) for i in range(8)])
    
    name = models.CharField(max_length=20)
    description = models.TextField()
    
    # @@@ initially no houses
    kind = models.CharField(max_length=1, choices = (('A', 'accessible'), ('I', 'inaccessible')))
    
    # @@@ eventually will have an image too
    
    def who_is_here(self): # @@@ can't wait for model inheritance
        players = set()
        for location in Location.objects.filter(lot=self, visible=True):
            players = players.union(location.player_set.all())
        return len(players), players
    
    def what_is_here(self):
        return [pile for pile in LocationPile.objects.filter(lot=self) if pile.total_quantity() > 0]
    
    def drop_here(self, item_type, quantity):
        pile, created = LocationPile.objects.get_or_create(item_type=item_type, hub=self.hub, lot=self, defaults={'quantity': 0})
        return pile.increase(quantity)
    
    class Meta:
        unique_together = (
            ('hub', 'position'),
        )
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass


class Location(models.Model):
    
    hub = models.ForeignKey(Hub)
    lot = models.ForeignKey(Lot, null=True)
    visible = models.BooleanField(default=True)
    
    def move_to_lot(self, lot):
        self.lot = lot
        self.hub = lot.hub
        self.save()
    
    def move_to_hub(self, hub):
        self.hub = hub
        self.lot = None
        self.save()
    
    def __unicode__(self):
        if self.lot:
            return "%s in %s" % (self.lot.name, self.hub.name)
        else:
            return self.hub.name