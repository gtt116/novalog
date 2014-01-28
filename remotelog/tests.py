import os
import os.path
import logging
import logging.handlers
import time
import datetime

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Permission

from remotelog import models as remotelog

class DjangoTestClientHandler(logging.handlers.HTTPHandler):
    """
    A class which sends log records to a Django view via the Django test client
    """
    def __init__(self, testcase, url, method='GET'):
        """
        Initialize the instance with the request URL, and the method
        ("GET" or "POST")
        """
        self.testcase = testcase
        logging.handlers.HTTPHandler.__init__(self, 'testserver', url, method)

    def emit(self, record):
        """
        Emit a record.

        Send the record to the Django view as an URL-encoded dictionary
        """
        data = self.mapLogRecord(record)
        client = Client()
        if self.method == 'GET':
            response = client.get(self.url, data)
        else:
            response = client.post(self.url, data)
        self.testcase.assertEqual(response.status_code, 200)
        self.testcase.assertContains(response, 'message saved')


class RemoteLogTest(TestCase):
    TEST_MESSAGE_DATA = {
        'relativeCreated': 3957.8011035899999,
        'process': 21389,
        'module': u'tests',
        'funcName': u'test_record_message',
        'date': datetime.datetime(2009, 6, 4, 17, 48, 12, 255545),
        'filename': u'tests.py', 
        'levelno': 10,
        'lineno': 67,
        'msg': u'test message',
        'remote_ip': u'127.0.0.1',
        'args': u'()',
        'exc_text': None,
        'name': u'remotelog',
        'thread': -1210210624.0,
        'created': 1244152092.24,
        'threadName': u'MainThread',
        'msecs': 240.50998687699999,
        'pathname': u'/path/to/remotelog/tests.py',
        'exc_info': None,
        'remote_host': u'',
        'levelname': u'DEBUG',
    }
    
    def setUp(self):
        self.application = remotelog.Application.objects.create(
            name='RemoteLog', 
            slug='remotelog',
        )
        self.logger = logging.getLogger('remotelog')
        url_kwargs = {
            'app_slug': self.application.slug,
        }
        url = reverse('create_message', kwargs=url_kwargs)
        handler = DjangoTestClientHandler(self, url, 'GET')
        handler.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
        
        self.user = User.objects.create_user(
            username='viewer',
            email='viewer@example.com',
            password='abc123',
        )
        view_message = Permission.objects.get(
            codename='view_message', 
            content_type__app_label='remotelog', 
            content_type__model='logmessage',
        )
        self.user.user_permissions.add(view_message)
        self.c = Client()
    
    def test_record_message(self):
        # log a message
        log_message = 'test message'
        self.logger.debug(log_message)
        
        # make sure it exists in the database
        self.assertEqual(self.application.messages.count(), 1)
        message = self.application.messages.all()[0]
        # this doesn't really work because sometimes __file__ is the pyc
        #self.assertEqual(message.pathname, __file__)
        #self.assertEqual(message.filename, os.path.basename(__file__))
        self.assertEqual(message.name, self.logger.name)
        self.assertEqual(message.msg, log_message)
        self.assertEqual(message.levelname, logging.getLevelName(logging.DEBUG))
    
    def test_view_message(self):
        log_message = 'test message'
        message = self.application.messages.create(**self.TEST_MESSAGE_DATA)
        
        # try to view the message before logging in
        url_kwargs = {
            'app_slug': self.application.slug,
            'message_id': message.id,
        }
        response = self.c.get(reverse('view_message', kwargs=url_kwargs))
        login_url_with_next = '%s?next=%s' % (
            reverse('auth_login'),
            reverse('view_message', kwargs=url_kwargs)
        )
        self.assertRedirects(response, login_url_with_next)
        
        # retry after logging in
        self.c.login(username=self.user.username, password='abc123')
        response = self.c.get(reverse('view_message', kwargs=url_kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, message.msg)
        
        
        
