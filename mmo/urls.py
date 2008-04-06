from django.conf.urls.defaults import *

import os.path

urlpatterns = patterns('',
    (r'^map/', include('mmo.map.urls')),
    (r'^player/', include('mmo.player.urls')),
    (r'^items/', include('mmo.items.urls')),
    (r'^chat/', include('mmo.chat.urls')),
    
    (r'^admin/', include('django.contrib.admin.urls')),
    
    # @@@ just for dev
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), "site_media")}),

)

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns("django.views",
        url(r"^static/(?P<path>.*)", "static.serve", {
            "document_root": settings.MEDIA_ROOT,
        })
    )
