from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^mmo/', include('mmo.foo.urls')),
    
     (r'^admin/', include('django.contrib.admin.urls')),
)
