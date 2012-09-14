from dateutil import parser
import simplejson
from StringIO import StringIO
import urllib2

from django.utils import unittest
from django.conf import settings

from mock import Mock

from ci_monitor.jenkins import jenkins
from ci_monitor.tests.test_support import generate_xml_doc, mock_url_open_conn_for_rss_feed, mock_url_open_job_last_build, generate_xml_doc_with_matrix

class ManualRetrieveTests(unittest.TestCase):
    
    def test_constructor_with_valid_argumetns(self):
        #test a normal constructor
        expected_hostname = 'http://localhost:8080'
        expected_jobname = 'Job1'
        job = jenkins.RetrieveJob(expected_hostname,expected_jobname)
        self.assertEqual(job.hostname,expected_hostname)
        self.assertEqual(job.jobname,expected_jobname)
        
    def test_construcotr_with_null_arguments(self):
        #test a constructor with null
        expected_hostname = None
        expected_jobname = None
        job = jenkins.RetrieveJob(expected_hostname,expected_jobname)
        self.assertEqual(job.hostname,expected_hostname)
        self.assertEqual(job.jobname,expected_jobname)
        
    def test_lookup_hostname_returns_url_error(self):
        #test lookup hostname that's an invalid URL
        jenkins.urllib2.urlopen = Mock(return_value=urllib2.URLError('bad-url'),side_effect=urllib2.URLError('bad url'))
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        self.assertEqual(type(job.lookup_hostname()),type(urllib2.URLError))
        
    def test_lookup_hostname_returns_value_error(self):
        #test lookup hostname that's an invalid URL
        jenkins.urllib2.urlopen = Mock(return_value=ValueError('bad-url'),side_effect=ValueError('bad url'))
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        self.assertEqual(type(job.lookup_hostname()),type(ValueError))
        
    def test_lookup_hostname_returns_True(self):
        #test lookup hostname works as expected
        jenkins.urllib2.urlopen = Mock(return_value=StringIO())
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        self.assertEqual(job.lookup_hostname(),True)
        
    def test_lookup_job_returns_ValueError(self):
        #test lookup job returns ValueError
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        jenkins.urllib2.urlopen = Mock(return_value=None,side_effect=ValueError('bad url'))
        job = jenkins.RetrieveJob(hostname,jobname)
        self.assertEqual(type(job.lookup_job()),type(ValueError))
        
    def test_lookup_job_returns_URLError(self):
        #test lookup job returns URLError
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        jenkins.urllib2.urlopen = Mock(return_value=StringIO(),side_effect=urllib2.URLError('bad url'))
        job = jenkins.RetrieveJob(hostname,jobname)
        self.assertEqual(type(job.lookup_job()),type(urllib2.URLError))
        
    def test_lookup_job_returns_True(self):
        #test lookup job works as expected
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        jenkins.urllib2.urlopen = Mock(return_value=mock_url_open_job_last_build())
        job = jenkins.RetrieveJob(hostname,jobname)
        self.assertEqual(job.lookup_job(),dict(jobname='Job1',status='SUCCESS'))