from django.shortcuts import render_to_response, get_object_or_404
import datetime
from mmo.player.models import Player
from mmo.chat.models import ChatMessage, ServerMessage

def chat(request):
    """ displays chat output """
    # FIXME: The way I'm combining querysets here seems hackish. Maybe I should go with MTI over ABC?
    global_messages = ChatMessage.objects.all()[:100]
    server_messages = ServerMessage.objects.all()[:100]
    all_msgs = global_messages
    all_msgs = [msg for msg in global_messages] + [msg for msg in server_messages]
    all_msgs.sort(key=lambda x:x.timestamp)
    
    return render_to_response('chat/chat_window.html', {'messages':all_msgs})

def update_chat(request, player_id):
    """ Method for inserting chat or returning recent chats """
    if request.method == "POST":
        player = Player.objects.get(pk=player_id)
        # User has submitted a message, so insert it.
        message = ChatMessage(message=request.POST['message'], from_player=player, timestamp=datetime.datetime.now())
        message.save()
        # Only keep the 100 most recent messages in the database
        # At least in development
        over_100 = ChatMessage.objects.order_by('-timestamp')[100:]
        if over_100 >= 0:
            over_100.delete()
    # Update the chat box now.
    else:
        player = Player.objects.get(pk=player_id)
        global_messages = ChatMessage.objects.all()[:100]
        server_messages = ServerMessage.objects.all()[:100]
        all_msgs = [msg for msg in global_messages] + [msg for msg in server_messages]
        all_msgs.sort(key=lambda x:x.timestamp)
        all_msgs.reverse()
    
    return render_to_response('chat/messages.html', {'messages':all_msgs, 'player':player})
