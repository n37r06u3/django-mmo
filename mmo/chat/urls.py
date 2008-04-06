from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'mmo.chat.views.chat'),
	(r'^chat/$', 'mmo.chat.views.chat'),
	(r'^update_chat/$', 'mmo.chat.views.update_chat'),
)
