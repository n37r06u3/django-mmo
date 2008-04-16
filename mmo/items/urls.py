from django.conf.urls.defaults import *

from models import *
from views import *

urlpatterns = patterns('django.views.generic.list_detail',
    (r'type/$', itemtype_list),
    (r'type/(\d+)/$', itemtype_detail),
)
urlpatterns += patterns('',
	(r'whatshere/(?P<player_id>\d+)/$', 'mmo.items.views.whats_here'),
)