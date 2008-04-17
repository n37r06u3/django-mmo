from django.shortcuts import render_to_response, get_object_or_404
import datetime
from mmo.player.models import Player
from mmo.chat.models import Chat

def chat(request):
	all_msgs = Chat.objects.order_by('-timestamp')
	
	return render_to_response('chat/chat_window.html', {'message':all_msgs})

def update_chat(request, player_id):	
	""" Method for inserting chat or returning recent chats """
	if request.method == "POST":
		player = Player.objects.get(pk=player_id)
		# User has submitted a message, so insert it.
		message = Chat(message=request.POST['message'], player=player, timestamp=datetime.datetime.now())
		message.save()
		# Only keep the 100 most recent messages in the database
		# At least in development
		last_100 = Chat.objects.order_by('-timestamp')[100:]
		last_100.delete()
	# Update the chat box now.
	else:
		player = Player.objects.get(pk=player_id)
	all_msgs = Chat.objects.order_by('-timestamp')
	
	return render_to_response('chat/messages.html', {'messages':all_msgs, 'player':player})	