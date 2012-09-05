from mock import Mock
from StringIO import StringIO
import urllib2

from django.utils import unittest
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.conf import settings

from ci_monitor.pull import views
from ci_monitor.tests.test_support import generate_xml_doc



class ViewTests(unittest.TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        doc = generate_xml_doc()
        ns = doc.tag.replace('feed','')
        elements = doc.findall('%sentry' % ns)
        elements = elements[:-1]

        self.rss_expected = (dict(
            hostname = 'http://localhost:8080/view/BVD/rssAll',
            elements = elements,
                    ),
                    ns)
    

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
		
    def test_retrieve_job_returns_404(self):
    	request = self.factory.post('/pull/retrieve_job', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    	views.RetrieveJob.lookup_job = Mock(return_value=ValueError)

    	expected = [dict(status = 404)]
    	actual = views.retrieve_job(request)

    	self.assertEqual(actual.content,simplejson.dumps(expected))
    	self.assertEqual(actual.status_code,200)

    def test_retrieve_job_returns_500(self):
    	request = self.factory.post('/pull/retrieve_job', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    	views.RetrieveJob.lookup_job = Mock(return_value=urllib2.URLError)
    	expected = [dict(status = 500)]

    	actual = views.retrieve_job(request)
    	self.assertEqual(actual.content,simplejson.dumps(expected))
    	self.assertEqual(actual.status_code,200)
    	
    def test_validate_hostname_returns_True(self):
        request = self.factory.post('/pull/validate_hostname', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        views.RetrieveJob.lookup_hostname = Mock(return_value=StringIO())
        expected = [dict(status = 200)]
        actual = views.validate_hostname(request)
        self.assertEqual(actual.content,simplejson.dumps(expected))
        self.assertEqual(actual.status_code,200)
        
    def test_retrieve_job_returns_200(self):

    	d = dict(jobname = 'Test1', status = 'SUCCESS')
    	views.RetrieveJob.lookup_job = Mock(return_value=d)
    	hostname = 'http://localhost:8080'
    	
    	expected = d.update(dict(hostname = hostname, status = 200))
    	
    	post_data = {'hostname' : hostname, 'jobname' : 'Test1'}

        request = self.factory.post('/pull/retrieve_job',data=post_data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    	actual = views.retrieve_job(request)
    	self.assertEqual(actual.content,simplejson.dumps(expected))
    	self.assertEqual(actual.status_code,200)
        
	
"""
    def test_poll_jenkins_view_with_no_post_data_when_host_gives_404(self):
        request = self.factory.post('/pull/get_jenkins_views', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            
        expected = []
        
        views.PollCI.read_rss = Mock(return_value=(None,urllib2.URLError))

        actual = views.poll_jenkins_servers(request)

        self.assertEqual(actual.content,simplejson.dumps(expected))
        self.assertEqual(actual.status_code,200)

    def test_poll_jenkins_view_with_no_post_data_when_host_gives_url_error(self):
        request = self.factory.post('/pull/get_jenkins_views',HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        expected = []
        views.PollCI.read_rss = Mock(return_value=(None,urllib2.HTTPError))

        actual = views.poll_jenkins_servers(request)

        self.assertEqual(actual.content,simplejson.dumps(expected))
        self.assertEqual(actual.status_code,200)
        
    def test_poll_jenkins_view_with_post_data_when_host_gives_url_error(self):
        #hosts = 'http://localhost:8080/view/BVD/rssAll'
        json = dict(   
                        job_name = "test1 #2",
                        status = "DOWN"
                    )
                    
        expected = [
            dict(
                hostname = 'ht://localhost:8080/view/BVD/rssAll',
                json = [json,json,json]
            )
        ]
        
        views.PollCI.read_rss = Mock(return_value=(None,urllib2.URLError))
        #views.PollCI.poll = Mock(return_value=json)
        
        post_data = {'hosts' : simplejson.dumps([{'ht://localhost:8080/view/BVD/rssAll' : [json,json,json]}])}

        request = self.factory.post('/pull/get_jenkins_views',data=post_data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        actual = views.poll_jenkins_servers(request)
        
        self.assertEqual(actual.content,simplejson.dumps(expected))
        self.assertEqual(actual.status_code,200)
        
    def test_poll_ci_function_with_tuple_parameter(self):
        hosts = 'http://localhost:8080/view/BVD/rssAll'
        json = dict(   
                        job_name = "test1 #2",
                        status = "FAILURE"
                    )
                    
        expected = [
            dict(
                hostname = 'http://localhost:8080/view/BVD/rssAll',
                json = [
                    json,
                    json,
                    json
                ]
            )
        ]
        
        views.PollCI.read_rss = Mock(return_value=self.rss_expected)
        views.PollCI.poll = Mock(return_value=json)
        
        actual = views.poll_ci((hosts,))
        self.assertEqual(actual,expected)
        
    def test_poll_ci_function_with_dict_parameter(self):
        json = dict(   
                    job_name = "test1 #2",
                    status = "FAILURE"
                )
                
        hosts = [dict(
                        hostname = 'http://localhost:8080/view/BVD/rssAll',
                        json =  [json,json,json],
                ),
        ]

        expected = [dict(
                hostname = 'http://localhost:8080/view/BVD/rssAll',
                json = [
                    json,
                    json,
                    json
                ]
            )]
     

        views.PollCI.read_rss = Mock(return_value=self.rss_expected)
        views.PollCI.poll = Mock(return_value=json)

        actual = views.poll_ci(hosts)
        self.assertEqual(actual,expected)
        
    def test_poll_jenkins_view_with_no_post_data_but_expected_results(self):
        #TODO: User reverse for URL to view matching    
        json = dict(   
                    job_name = "test1 #2",
                    status = "FAILURE"
                )

        expected = [
            dict(
                hostname = 'http://localhost:8080/view/BVD/rssAll',
                json = [json,json,json]
            ),
            dict(
                hostname = 'http://localhost:8080/view/BVD/rssAll',
                json = [json,json,json]
            )
        ]

        views.PollCI.read_rss = Mock(return_value=self.rss_expected)
        views.PollCI.poll = Mock(return_value=json)
        request = self.factory.post('/pull/get_jenkins_views',HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        actual = views.poll_jenkins_servers(request)

        self.assertEqual(actual.content,simplejson.dumps(expected))
        self.assertEqual(actual.status_code,200)
"""