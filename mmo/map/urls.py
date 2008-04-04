from django.conf.urls.defaults import *

from models import Hub

hub_list_info = {
    'queryset': Hub.objects.all(),
    'template_object_name': 'hub'
}

hub_detail_info = hub_list_info

urlpatterns = patterns('django.views.generic.list_detail',
    (r'hub/$', 'object_list', hub_list_info),
    (r'hub/(?P<object_id>\d+)/$', 'object_detail', hub_detail_info),
)
