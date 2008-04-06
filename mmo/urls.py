from django.conf.urls.defaults import *

import os.path

urlpatterns = patterns('',
    (r'^map/', include('mmo.map.urls')),
    (r'^player/', include('mmo.player.urls')),
    (r'^items/', include('mmo.items.urls')),
    
    (r'^admin/', include('django.contrib.admin.urls')),
    
    # @@@ just for dev
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), "site_media")}),

)
