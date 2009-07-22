from django.conf.urls.defaults import *

from django.conf import settings

urlpatterns = patterns('',
    (r'', include('testproj.app.urls')),

    # django-flash needs to ignore requests to static files, in development mode
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', \
          {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
