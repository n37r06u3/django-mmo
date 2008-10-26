from django.contrib import admin
from mmo.chat.models import ChatMessage, ServerMessage

admin.site.register(ChatMessage)
admin.site.register(ServerMessage)
