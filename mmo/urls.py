from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^map/', include('mmo.map.urls')),
    
    (r'^admin/', include('django.contrib.admin.urls')),
)
