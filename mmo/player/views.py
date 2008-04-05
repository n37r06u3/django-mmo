from django.shortcuts import render_to_response, get_object_or_404

from models import Player
from map.models import *
from items.models import LocationPile

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
        # pickup_pile
        elif "pickup_pile" in request.POST:
            # @@@ check pile is here and quantity is valid
            pile_id = request.POST["pickup_pile"]
            pile = LocationPile.objects.get(id=pile_id)
            quantity = int(request.POST["quantity"])
            pile.reduce(quantity)
            # @@@ add to inventory
            
    return render_to_response("player/player_detail.html", {
        "player": player,
    })