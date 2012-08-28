from StringIO import StringIO

from django.utils import unittest
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.utils import simplejson

from ci_monitor.pull import views

class ViewTests(unittest.TestCase):
	
	def setUp(self):
		self.factory = RequestFactory()
		
	def test_poll_jenkins_view(self):
		expected = [
			dict(	
				job_name = "test1 #2",
				status = "FAILURE"
			),
			dict(
				job_name = "test3 #1",
				status = "SUCCESS"
				),
			dict(
				job_name = "test2 #1",
				status = "SUCCESS"
				)
			
		]
		#request = self.factory.get(reverse('poll_jenkins_view'))
		request = self.factory.get('/pull/get_jenkins_views',HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		actual = views.poll_jenkins_servers(request)
		
		self.assertEqual(actual.content,simplejson.dumps(expected))
		self.assertEqual(actual.status_code,200)
