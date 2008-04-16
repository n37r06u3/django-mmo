from django.conf.urls.defaults import *

from models import *
from views import *

urlpatterns = patterns('django.views.generic.list_detail',
    (r'type/$', itemtype_list),
    (r'type/(\d+)/$', itemtype_detail),
)
