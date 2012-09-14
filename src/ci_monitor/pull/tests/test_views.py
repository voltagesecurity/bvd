
from mock import Mock
from StringIO import StringIO
import urllib2

from django.utils import unittest
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson
from django.conf import settings
from django.contrib.auth.models import User

from ci_monitor.pull import views
from ci_monitor.pull import models
from ci_monitor.tests.test_support import generate_xml_doc



class ViewTests(unittest.TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()

        d1 = dict(hostname= 'http://pydevs.org:9080')
        d3 = dict(jobname = 'Test1')
        d2 = dict(displayname = 'Test1', left = '100px', top = '100px')
        
        
        self.server1 = models.CiServer(**d1)
        self.job1 = models.CiJob(**d3)
        
        
        
        self.server1.save()
        
        self.job1.ci_server = self.server1
        self.job1.save()
        
        

    def test_validate_hostname_returns_404(self):
		request = self.factory.post('/pull/validate_hostname', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		views.RetrieveJob.lookup_hostname = Mock(return_value=ValueError)
		
		expected = [dict(status = 404)]
		actual = views.validate_hostname(request)
		
		self.assertEqual(actual.content,simplejson.dumps(expected))
		self.assertEqual(actual.status_code,200)
    
        
    def test_validate_hostname_returns_500(self):
		request = self.factory.post('/pull/validate_hostname', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		views.RetrieveJob.lookup_hostname = Mock(return_value=urllib2.URLError)
		expected = [dict(status = 500)]
		
		actual = views.validate_hostname(request)
		self.assertEqual(actual.content,simplejson.dumps(expected))
		self.assertEqual(actual.status_code,200)
        
    
		
    def test_validate_job_returns_404(self):
        hostname = 'http://localhost:8080'
    	post_data = {'hostname' : hostname, 'jobname' : 'Test1'}
    	request = self.factory.post('/pull/validate_job',data=post_data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    	
    	views.RetrieveJob.lookup_job = Mock(return_value=ValueError)

    	expected = [dict(status = 404)]
    	actual = views.validate_job(request)

    	self.assertEqual(actual.content,simplejson.dumps(expected))
    	self.assertEqual(actual.status_code,200)

    
    def test_validate_job_returns_500(self):
        
        expected = [dict(status = 500)]
    	views.RetrieveJob.lookup_job = Mock(return_value=urllib2.URLError)
    	hostname = 'http://localhost:8080'
    	post_data = {'hostname' : hostname, 'jobname' : 'Test1'}
    	request = self.factory.post('/pull/validate_job',data=post_data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    	
    	views.RetrieveJob.lookup_job = Mock(return_value=urllib2.URLError)
    	actual = views.validate_job(request)
    	
    	self.assertEqual(actual.content,simplejson.dumps(expected))
    	self.assertEqual(actual.status_code,200)
    	
    
    
    def test_validate_hostname_returns_True(self):
        request = self.factory.post('/pull/validate_hostname', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        views.RetrieveJob.lookup_hostname = Mock(return_value=StringIO())
        expected = [dict(status = 200)]
        actual = views.validate_hostname(request)
        self.assertEqual(actual.content,simplejson.dumps(expected))
        self.assertEqual(actual.status_code,200)
        
    
    
    def test_validate_job_returns_200(self):

    	d = dict(jobname = 'Test1', status = 'SUCCESS')
    	views.RetrieveJob.lookup_job = Mock(return_value=d)
    	hostname = 'http://localhost:8080'
    	
    	expected = [dict(status = 200)]
    	
    	post_data = {'hostname' : hostname, 'jobname' : 'Test1'}

        request = self.factory.post('/pull/validate_job',data=post_data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.session = dict()

    	actual = views.validate_job(request)
    	
    	self.assertEqual(actual.content,simplejson.dumps(expected))
    	self.assertEqual(actual.status_code,200)
    	
    
    
    def test_validate_job_returns_500_when_invalid_request_data(self):
        
    	expected = [dict(status = 500)]
    	views.RetrieveJob.lookup_job = Mock(return_value=urllib2.URLError)
    	hostname = 'http://localhost:8080'
    	post_data = {'jobname' : 'Test1'}
    	request = self.factory.post('/pull/validate_job',data=post_data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    	
    	views.RetrieveJob.lookup_job = Mock(return_value=urllib2.URLError)
    	actual = views.validate_job(request)
    	
    	self.assertEqual(actual.content,simplejson.dumps(expected))
    	self.assertEqual(actual.status_code,200)
        
    
    	
    def test_retrieve_job_returns_500_when_invalid_request_data(self):
        
        expected = [dict(status = 500)]
    	
    	hostname = 'http://localhost:8080'
    	post_data = {'jobname' : 'Test1'}
    	request = self.factory.post('/pull/retrieve_job',data=post_data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = Mock(returnValue=User())
        request.user.is_authenticated = Mock(returnValue=True)
    	
    	actual = views.retrieve_job(request)
    	
    	self.assertEqual(actual.content,simplejson.dumps(expected))
    	self.assertEqual(actual.status_code,200)
    	

    	

    def test_retrieve_job_returns_200_when_user_is_authenticated(self):
        d = dict(jobname = 'Test2', status = 'SUCCESS')
    	hostname = 'http://localhost:8080'
    	post_data = {'hostname' : hostname, 'jobname' : 'Test2', 'displayname' : 'Test2'}
    	d.update(dict(hostname = hostname, status = 200))
    	request = self.factory.post('/pull/retrieve_job',data=post_data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        request.session = {'http://localhost:8080/Test2' : d}
        user = User(username='sammohamed')
        user.save()
        request.user = user 
        request.user.is_authenticated = Mock(returnValue=True)
        
    	actual = views.retrieve_job(request)
    	
    	self.assertEqual(actual.content,simplejson.dumps([d]))
    	self.assertEqual(actual.status_code,200)
    	
    	
    def test_autocomplete_hostname_expected_result(self):
        
        expected = ['http://pydevs.org:9080']
        
        views.models.CiServer.objects.get = Mock(return_value=self.server1)
    	post_data = {'txt' : 'pyd'}

        request = self.factory.post('/pull/autocomplete_hostname',data=post_data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    	actual = views.autocomplete_hostname(request)

    	self.assertEqual(actual.content,simplejson.dumps(expected))
    	self.assertEqual(actual.status_code,200)