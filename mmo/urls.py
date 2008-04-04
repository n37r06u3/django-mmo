from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^map/', include('mmo.map.urls')),
    (r'^player/', include('mmo.player.urls')),
    
    (r'^admin/', include('django.contrib.admin.urls')),
)
