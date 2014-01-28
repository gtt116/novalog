import pprint

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import permission_required

from remotelog.forms import LogMessageForm
from remotelog import models as remotelog

def create_message(request, app_slug):
    application = get_object_or_404(remotelog.Application, slug=app_slug)
    form = LogMessageForm(request, application)
    if form.is_valid():
        form.save()
        return HttpResponse('message saved')
    else:
        return HttpResponse(pprint.pformat(form.errors))

@permission_required('remotelog.view_message')
def view_message(request, app_slug, message_id):
    message = get_object_or_404(
        remotelog.LogMessage, 
        pk=message_id,
        application__slug=app_slug,
    )
    
    exc_text = message.exc_text
    pygments_css = None
    if exc_text:
        try:
            from pygments import highlight
            from pygments.lexers import PythonTracebackLexer
            from pygments.formatters import HtmlFormatter
            formatter = HtmlFormatter()
            exc_text = highlight(exc_text, PythonTracebackLexer(), formatter)
            pygments_css = formatter.get_style_defs('.highlight')
        except ImportError:
            pass
    
    opts = remotelog.LogMessage._meta
    context = {
        'message': message,
        'exc_text': exc_text,
        'pygments_css': pygments_css,
        
        # admin stuff
        'has_change_permission': True,
        'add': True,
        'change': True,
        'opts': opts,
        'app_label': opts.app_label,
    }
    return render_to_response('remotelog/view_message.html', context)