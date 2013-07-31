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
from django.test.client import RequestFactory, Client
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import User

from bvd.pull import views
from bvd.pull import models
from bvd.tests.test_support import generate_xml_doc


class ViewTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.user = User.objects.create_user('testuser', 'testuser@testuser.com', 'testpassword')
        self.user.save()

        self.testclient = Client()

    @classmethod
    def tearDownClass(self):
        User.objects.all().delete()

    def setUp(self):
        self.factory = RequestFactory()

        d1 = dict(hostname= 'http://pydevs.org:9080')
        d3 = dict(jobname = 'Test1')
        d2 = dict(displayname = 'Test1', jobname='Test1', width = '100px', height = '100px', user = self.user)
        
        self.server1 = models.CiServer(**d1)
        self.job1 = models.UserCiJob(**d2)
        
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
    	post_data = {'jobname' : 'Test1', 'user_id': 1}
    	request = self.factory.post('/pull/validate_job',data=post_data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    	
    	views.RetrieveJob.lookup_job = Mock(return_value=urllib2.URLError)
    	actual = views.validate_job(request)
    	
    	self.assertEqual(actual.content,simplejson.dumps(expected))
    	self.assertEqual(actual.status_code,200)
    	
    def test_autocomplete_hostname_expected_result(self):
        
        expected = ['http://pydevs.org:9080']
        
        views.models.CiServer.objects.get = Mock(return_value=self.server1)
    	post_data = {'txt' : 'pyd'}

        request = self.factory.post('/pull/autocomplete_hostname',data=post_data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    	actual = views.autocomplete_hostname(request)

    	self.assertEqual(actual.content,simplejson.dumps(expected))
    	self.assertEqual(actual.status_code,200)

    def test_save_widget_redirects_when_user_is_authenticated(self):
        request = self.factory.post('/pull/save_widget', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user
        request.user.is_authenticated = Mock(return_value=True)

        response = views.save_widget(request)

        self.assertEqual(response.status_code, 302)

    def test_save_widget_returns_401_when_unauthorized(self):
        request = self.factory.post('/pull/save_widget', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user
        request.user.is_authenticated = Mock(return_value=False)

        request.POST['widget_id'] = False
        response = views.save_widget(request)

        self.assertEqual(response.status_code,401)

    def test_save_widget_updates_fields_when_provided(self):
        request = self.factory.post('/pull/save_widget', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user
        request.user.is_authenticated = Mock(return_value=True)

        request.POST['displayname'] = "new-italiandisplay"
        request.POST['jobname'] = "new-italianjob"
        request.POST['widget_id'] = self.job1.pk

        response = views.save_widget(request)

        widget = models.UserCiJob.objects.get(pk=self.job1.pk)

        self.assertEqual(widget.displayname, "new-italiandisplay")
        self.assertEqual(widget.jobname, "new-italianjob")

    def test_save_widget_makes_active_when_post_data_defined(self):
        request = self.factory.post('/pull/save_widget', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user
        request.user.is_authenticated = Mock(return_value=True)

        request.POST['widget_id'] = self.job1.pk
        request.POST['entity_active'] = '1'

        response = views.save_widget(request)

        widget = models.UserCiJob.objects.get(pk=self.job1.pk)

        self.assertTrue(widget.entity_active)

    def test_save_widget_makes_inactive_when_post_data_undefined(self):
        request = self.factory.post('/pull/save_widget', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user
        request.user.is_authenticated = Mock(return_value=True)

        request.POST['widget_id'] = self.job1.pk
        # request.POST['entity_active'] = '1'
        # (commented out for verbosity)
        # since 'entity_active' won't be in the POST dict, the widget will be set to inactive

        response = views.save_widget(request)

        widget = models.UserCiJob.objects.get(pk=self.job1.pk)

        self.assertFalse(widget.entity_active)

    def test_save_widget_updates_ci_server_when_provided(self):
        request = self.factory.post('/pull/save_widget', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user
        request.user.is_authenticated = Mock(return_value=True)

        newhostname = "http://newciserver:8080"
        server2 = models.CiServer(hostname=newhostname)
        server2.save()

        request.POST['ci_server'] = server2.hostname
        request.POST['widget_id'] = self.job1.pk

        response = views.save_widget(request)

        widget = models.UserCiJob.objects.get(pk=self.job1.pk)

        self.assertEqual(widget.ci_server.hostname, newhostname)

    def test_save_widget_creates_and_updates_ci_server_when_new_server_provided(self):
        request = self.factory.post('/pull/save_widget', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user
        request.user.is_authenticated = Mock(return_value=True)

        newhostname = "http://reallynewciserver:8080"

        request.POST['new_ci_server'] = newhostname
        request.POST['widget_id'] = self.job1.pk

        response = views.save_widget(request)

        widget = models.UserCiJob.objects.get(pk=self.job1.pk)

        self.assertEqual(widget.ci_server.hostname, newhostname)

    def test_add_job_error_when_unauthenticated(self):
        request = self.factory.post('/pull/save_widget', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user
        request.user.is_authenticated = Mock(return_value=False)

        response = views.save_widget(request)

        self.assertEqual(response.status_code, 401)

    def test_add_job_redirects_when_authenticated(self):
        request = self.factory.post('/pull/save_widget', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user
        request.user.is_authenticated = Mock(return_value=True)

        response = views.save_widget(request)

        self.assertEqual(response.status_code, 302)

    def test_add_job_creates_job_when_authenticated_and_data_provided(self):
        request = self.factory.post('/pull/save_widget', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user
        request.user.is_authenticated = Mock(return_value=True)

        request.POST['ci_server'] = self.server1.hostname
        request.POST['jobname'] = "add_job_test"
        request.POST['displayname'] = "add_job_test_displayname"

        response = views.add_job(request)

        widget = models.UserCiJob.objects.get(jobname=request.POST['jobname'])

        self.assertEqual(widget.displayname, request.POST['displayname'])

        widget.delete()

    def test_add_job_uses_jobname_for_displayname_when_displayname_not_provided(self):
        request = self.factory.post('/pull/save_widget', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user
        request.user.is_authenticated = Mock(return_value=True)

        request.POST['ci_server'] = self.server1.hostname
        request.POST['jobname'] = "add_job_test"

        response = views.add_job(request)

        widget = models.UserCiJob.objects.get(jobname=request.POST['jobname'])

        self.assertEqual(widget.displayname, request.POST['jobname'])

        widget.delete()

    def test_add_job_updates_job_when_exists(self):
        request = self.factory.post('/pull/save_widget', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user
        request.user.is_authenticated = Mock(return_value=True)

        request.POST['ci_server'] = self.server1.hostname
        request.POST['jobname'] = "add_job_test"
        request.POST['displayname'] = "before-update"

        response = views.add_job(request)
        
        request.POST['displayname'] = "after-update"
        response = views.add_job(request)

        widget = models.UserCiJob.objects.get(jobname=request.POST['jobname'])

        self.assertEqual(widget.displayname, "after-update")

        widget.delete()


    def test_widget_to_dictionary_throws_when_not_usercijob_instance(self):
        exception_raised = False
        try:
            views.widget_to_dictionary(1)
        except TypeError:
            exception_raised = True
        self.assertTrue(exception_raised)

    def test_widget_to_dictionary_returns_dictionary_when_usercijob_instance(self):
        self.assertEqual(type(views.widget_to_dictionary(self.job1)), type(dict()))

    def test_widget_to_dictionary_returns_complete_dictionary_when_usercijob_instance(self):
        proper_data = dict(
            pk = self.job1.pk,
            ci_server = self.job1.ci_server.pk,
            hostname = self.job1.ci_server.hostname,
            jobname = self.job1.jobname,
            displayname = self.job1.displayname,
            width = self.job1.width,
            height = self.job1.height,
            status = self.job1.status,
            readonly = self.job1.readonly,
            icon = self.job1.icon,
            user = self.job1.user.pk,
            entity_active = self.job1.entity_active,
            appletv = self.job1.appletv,
            appletv_active = self.job1.appletv_active,
        )
        self.assertEqual(views.widget_to_dictionary(self.job1), proper_data)


