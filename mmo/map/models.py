from django.db import models

class Hub(models.Model):
    
    name = models.CharField(max_length=20)
    description = models.TextField()
    
    # @@@ eventually this will have an x, y location for the visual map
    
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

