from django.contrib import admin
from mmo.items.models import ItemType, LocationPile, MakeTarget, MakeIngredient

admin.site.register(ItemType)
admin.site.register(LocationPile)
admin.site.register(MakeTarget)
admin.site.register(MakeIngredient)