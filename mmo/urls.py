from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

import os.path

urlpatterns = patterns('',
    (r'^map/', include('mmo.map.urls')),
    (r'^player/', include('mmo.player.urls')),
    (r'^items/', include('mmo.items.urls')),
    (r'^chat/', include('mmo.chat.urls')),
    
    (r'^admin/(.*)', admin.site.root),
)

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns("django.views",
        url(r"^static/(?P<path>.*)", "static.serve", {
            "document_root": os.path.join(os.path.dirname(__file__), "site_media"),
        })
    )
