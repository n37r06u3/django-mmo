from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'mmo.chat.views.chat'),
	(r'^chat/$', 'mmo.chat.views.chat'),
	(r'^update_chat/(?P<player_id>\d+)/$', 'mmo.chat.views.update_chat'),
)
