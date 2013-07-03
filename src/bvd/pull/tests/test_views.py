"""
BVD v1.0

Copyright (c) 2012 Voltage Security
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. The name of the author may not be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from mock import Mock, patch
from StringIO import StringIO
import urllib2

from django.utils import unittest
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson
from django.conf import settings
from django.contrib.auth.models import User

from bvd.pull import views
from bvd.pull import models
from bvd.tests.test_support import generate_xml_doc



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
        
        

    @patch('bvd.jenkins.jenkins.RetrieveJob.lookup_hostname', Mock(return_value=ValueError))
    def test_validate_hostname_returns_404(self):
		request = self.factory.post('/pull/validate_hostname', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		
		expected = [dict(status = 404)]
		actual = views.validate_hostname(request)
		
		self.assertEqual(actual.content,simplejson.dumps(expected))
		self.assertEqual(actual.status_code,200)
    
        
    @patch('bvd.jenkins.jenkins.RetrieveJob.lookup_hostname', Mock(return_value=urllib2.URLError))
    def test_validate_hostname_returns_500(self):
		request = self.factory.post('/pull/validate_hostname', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		expected = [dict(status = 500)]
		
		actual = views.validate_hostname(request)
		self.assertEqual(actual.content,simplejson.dumps(expected))
		self.assertEqual(actual.status_code,200)
        
    
		
    @patch('bvd.jenkins.jenkins.RetrieveJob.lookup_job', Mock(return_value=ValueError))
    def test_validate_job_returns_404(self):
        hostname = 'http://localhost:8080'
    	post_data = {'hostname' : hostname, 'jobname' : 'Test1'}
    	request = self.factory.post('/pull/validate_job',data=post_data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    	
    	expected = [dict(status = 404)]
    	actual = views.validate_job(request)

    	self.assertEqual(actual.content,simplejson.dumps(expected))
    	self.assertEqual(actual.status_code,200)

    
    @patch('bvd.jenkins.jenkins.RetrieveJob.lookup_job', Mock(return_value=urllib2.URLError))
    def test_validate_job_returns_500(self):
        
        expected = [dict(status = 500)]
    	hostname = 'http://localhost:8080'
    	post_data = {'hostname' : hostname, 'jobname' : 'Test1'}
    	request = self.factory.post('/pull/validate_job',data=post_data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    	
    	views.RetrieveJob.lookup_job = Mock(return_value=urllib2.URLError)
    	actual = views.validate_job(request)
    	
    	self.assertEqual(actual.content,simplejson.dumps(expected))
    	self.assertEqual(actual.status_code,200)
    	
    
    
    @patch('bvd.jenkins.jenkins.RetrieveJob.lookup_hostname', Mock(return_value=StringIO()))
    def test_validate_hostname_returns_True(self):
        request = self.factory.post('/pull/validate_hostname', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        expected = [dict(status = 200)]
        actual = views.validate_hostname(request)
        self.assertEqual(actual.content,simplejson.dumps(expected))
        self.assertEqual(actual.status_code,200)
        
    
    
    @patch('bvd.jenkins.jenkins.RetrieveJob.lookup_job', \
            Mock(return_value=dict(jobname = 'Test1', status = 'SUCCESS')))
    def test_validate_job_returns_200(self):
    	hostname = 'http://localhost:8080'
    	
    	expected = [dict(status = 200)]
    	
    	post_data = {'hostname' : hostname, 'jobname' : 'Test1'}

        request = self.factory.post('/pull/validate_job',data=post_data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.session = dict()

    	actual = views.validate_job(request)
    	
    	self.assertEqual(actual.content,simplejson.dumps(expected))
    	self.assertEqual(actual.status_code,200)
    	
    
   
    @patch('bvd.jenkins.jenkins.RetrieveJob.lookup_job', Mock(return_value=urllib2.URLError))
    def test_validate_job_returns_500_when_invalid_request_data(self):
        
    	expected = [dict(status = 500)]
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
