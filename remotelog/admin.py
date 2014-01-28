from django.contrib import admin
from django.core.urlresolvers import reverse

from remotelog import models as remotelog


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name', 'slug',)
admin.site.register(remotelog.Application, ApplicationAdmin)

#    date = models.DateTimeField()
#    remote_ip = models.CharField(max_length=40)
#    remote_host = models.CharField(max_length=255)
#    
#    levelno = models.IntegerField()
#    levelname = models.CharField(max_length=255)
#    
#    name = models.CharField(max_length=255)
#    module = models.CharField(max_length=255)
#    filename = models.CharField(max_length=255)
#    pathname = models.CharField(max_length=255)
#    funcName = models.CharField(max_length=255)
#    lineno = models.IntegerField()
#    
#    msg = models.TextField()
#    exc_info = models.TextField()
#    exc_text = models.TextField()
#    args = models.TextField(null=True, blank=True)
#    
#    threadName = models.CharField(max_length=255)
#    thread = models.FloatField()
#    created = models.FloatField()
#    process = models.IntegerField()
#    relativeCreated = models.FloatField()
#    msecs = models.FloatField()

class LogMessageAdmin(admin.ModelAdmin):
    list_display = ('application', 'date', 'remote_ip', 'name', 'levelname', 'short_msg', 'view_link')
    search_fields = ('remote_ip', 'remote_host', 'name', 'filename', 'funcName', 'levelname', 'short_msg')
    list_filter = ('application', 'remote_ip', 'levelname', 'name', 'date',)
    
    def short_msg(self, obj):
        return obj.short_msg
    short_msg.short_description = 'Message'
    
    def view_link(self, obj):
        kwargs = {
            'message_id': obj.id,
            'app_slug': obj.application.slug,
        }
        return '<a href="%s">View</a>' % reverse('view_message', kwargs=kwargs)
    view_link.short_description = ''
    view_link.allow_tags = True

admin.site.register(remotelog.LogMessage, LogMessageAdmin)