from django.db import models

class Player(models.Model):
    
    name = models.CharField(max_length=20)
    
    location = models.ForeignKey('map.Location')
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass