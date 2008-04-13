from django.conf.urls.defaults import *

from models import *
from views import *

urlpatterns = patterns('',
    (r'^$', player_list),
    (r'^(\d+)/$', player_view),
	# @@@ I don't like this living here. I'd rather it be in map
	(r'^who_is_here/(?P<player_id>\d+)/$', who_is_here),
)
