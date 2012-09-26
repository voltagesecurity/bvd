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
from dateutil import parser
import simplejson
from StringIO import StringIO
import urllib2

from django.utils import unittest
from django.conf import settings

from mock import Mock

from bvd.jenkins import jenkins
from bvd.tests.test_support import generate_xml_doc, mock_url_open_conn_for_rss_feed, \
                                            mock_url_open_job_last_build, generate_xml_doc_with_matrix

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