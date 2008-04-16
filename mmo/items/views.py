from django.shortcuts import render_to_response, get_object_or_404
from mmo.player.models import Player
from models import *

def itemtype_list(request):
    
    if request.POST:
        name = request.POST["name"]
        description = request.POST["description"]
        itemtype = ItemType(name=name, description=description)
        itemtype.save()
    
    itemtype_list = ItemType.objects.all()
    
    return render_to_response("items/itemtype_list.html", {
        "itemtype_list": itemtype_list,
    })


def itemtype_detail(request, itemtype_id):
    itemtype = get_object_or_404(ItemType, id=itemtype_id)
    
    if request.POST:
        pass # @@@ for now

    return render_to_response("items/itemtype_detail.html", {
        "itemtype": itemtype,
    })
def whats_here(request, player_id):
	# @@@ for the purposes of this activity, I'd like LocationPile to use Location, not hub/lot
	player = get_object_or_404(Player, id=player_id)
	if player.location.lot != None:
		obj_list = LocationPile.objects.filter(hub=player.location.hub, lot=player.location.lot)
	else:
		obj_list = LocationPile.objects.filter(hub=player.location.hub, lot__isnull=True)
	return render_to_response('items/whatshere.html', {'objects':obj_list})