from django.db import models
from django.core.urlresolvers import reverse

class Application(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name


class LogMessage(models.Model):
    application = models.ForeignKey(Application, related_name='messages')
    
    date = models.DateTimeField()
    remote_ip = models.CharField(max_length=40)
    remote_host = models.CharField(max_length=255)
    
    levelno = models.IntegerField()
    levelname = models.CharField(max_length=255)
    
    name = models.CharField(max_length=255)
    module = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    pathname = models.CharField(max_length=255)
    funcName = models.CharField(max_length=255)
    lineno = models.IntegerField()
    
    msg = models.TextField()
    exc_info = models.TextField(null=True, blank=True)
    exc_text = models.TextField(null=True, blank=True)
    args = models.TextField(null=True, blank=True)
    
    threadName = models.CharField(max_length=255)
    thread = models.FloatField()
    created = models.FloatField()
    process = models.IntegerField()
    relativeCreated = models.FloatField()
    msecs = models.FloatField()
    
    def get_absolute_url(self):
        url_kwargs = {
            'app_slug': self.application.slug,
            'message_id': self.id,
        }
        return reverse('view_message', kwargs=url_kwargs)
    
    def _get_short_msg(self):
        msg = self.msg[0:60] 
        if len(self.msg) > 60:
            msg += '...'
        return msg
    short_msg = property(_get_short_msg)
    
    class Meta:
        # order by date and then (theoretically) creation order
        ordering = ('-date', '-id')
        permissions = (
            ("view_message", "Can view log messages"),
        )

    def __unicode__(self):
        return '%s: %s' % (self.date, self.short_msg)