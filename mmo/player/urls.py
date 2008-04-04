from django.conf.urls.defaults import *

from models import *
from views import player_view

player_list_info = {
    'queryset': Player.objects.all(),
    'template_object_name': 'player'
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', player_list_info),
    (r'^(\d+)/$', player_view),
)
