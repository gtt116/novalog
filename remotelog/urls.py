from django.conf.urls.defaults import *

urlpatterns = patterns('remotelog.views',
    url(
        r'^(?P<app_slug>[\w-]+)/log/$', 
        'create_message', 
        name="create_message",
    ),
    url(
        r'^(?P<app_slug>[\w-]+)/message/(?P<message_id>\d+)/$', 
        'view_message', 
        name="view_message",
    ),
)
