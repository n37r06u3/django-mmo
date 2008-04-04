from django.shortcuts import render_to_response, get_object_or_404

from models import Player
from map.models import *

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
            
    return render_to_response("player/player_detail.html", {
        "player": player,
    })