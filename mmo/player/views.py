from django.shortcuts import render_to_response, get_object_or_404

from models import *
from map.models import *
from items.models import *

def player_list(request):
    
    if request.POST:
        name = request.POST["name"]
        start_hub_id = request.POST["start_hub"]
        hub = Hub.objects.get(id=start_hub_id)
        location = Location(hub=hub)
        location.save()
        player = Player(name=name, location=location)
        player.save()
    
    player_list = Player.objects.all()
    hubs = Hub.objects.all()
    
    return render_to_response("player/player_list.html", {
        "player_list": player_list,
        "hubs": hubs,
    })

def player_view(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    
    if request.POST:
        # enter, exit_to, travel_to
        if "travel_to" in request.POST:
            destination_id = request.POST["travel_to"]
            # @@@ check there is a road to there
            destination = Hub.objects.get(id=destination_id)
            player.location.move_to_hub(destination)
        elif "enter" in request.POST:
            destination_id = request.POST["enter"]
            # @@@ check the lot is off this hub
            destination = Lot.objects.get(id=destination_id)
            player.location.move_to_lot(destination)
        elif "exit_to" in request.POST:
            destination_id = request.POST["exit_to"]
            # @@@ check the hub is off this lot
            destination = Hub.objects.get(id=destination_id)
            player.location.move_to_hub(destination)
        # pickup_pile, drop_pile
        elif "pickup_pile" in request.POST:
            # @@@ check pile is here and quantity is valid
            pile_id = request.POST["pickup_pile"]
            pile = LocationPile.objects.get(id=pile_id)
            quantity = int(request.POST["quantity"])
            pile.reduce(quantity)
            player.add_to_inventory(pile.item_type, quantity)
        elif "drop_pile" in request.POST:
            # @@@ check pile belongs to player and quantity is valid
            pile_id = request.POST["drop_pile"]
            pile = InventoryPile.objects.get(id=pile_id) # @@@ will throw exception if quantity not checked
            quantity = int(request.POST["quantity"])
            pile.reduce(quantity)
            if player.location.lot:
                player.location.lot.drop_here(pile.item_type, quantity)
            else:
                player.location.hub.drop_here(pile.item_type, quantity)
        elif "make_target" in request.POST:
            # @@@ need to double check can actually be made
            target_id = request.POST["make_target"]
            target = MakeTarget.objects.get(id=target_id) # @@@ may throw exception
            player.make(target)
        else:
            print "UNRECOGNIZED POST: %s" % request.POST.keys()
    return render_to_response("player/player_detail.html", {
        "player": player,
    })