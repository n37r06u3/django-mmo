from django.conf.urls.defaults import *

from models import *
from views import *

urlpatterns = patterns('',
    (r'^$', player_list),
    (r'^(\d+)/$', player_view),
)
