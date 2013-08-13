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
import datetime
import simplejson
from StringIO import StringIO
import urllib2

from django.utils import unittest
from django.conf import settings

from mock import Mock, patch

from bvd.jenkins import jenkins
from bvd.tests.test_support import *

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
        
    @patch('urllib2.urlopen', Mock(return_value=None,side_effect=ValueError('bad url')))
    def test_lookup_job_returns_ValueError(self):
        #test lookup job returns ValueError
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        self.assertEqual(type(job.lookup_job()),type(ValueError))
    
    @patch('urllib2.urlopen', Mock(return_value=StringIO(),side_effect=urllib2.URLError('bad url')))
    def test_lookup_job_returns_URLError(self):
        #test lookup job returns URLError
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        self.assertEqual(type(job.lookup_job()),type(urllib2.URLError))
        
    @patch('urllib2.urlopen', Mock(return_value=mock_url_open_job_last_build()))
    def test_lookup_job_returns_True(self):
        #test lookup job works as expected
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        self.assertEqual(job.lookup_job(),dict(jobname='Job1',status='SUCCESS'))

    @patch('urllib2.urlopen', mock_url_open_last_successful_build)
    def test_lookup_last_successful_build_returns_dictionary_when_success(self):
        # Tests that lookup_last_successful_build() pulls from Jenkins server with
        # host and job names for overall job data (I.E. not a specific job number or
        # the last build) to get lastSuccessfulBuild from json
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        data = job.lookup_last_successful_build()
        self.assertEqual(type(data),type(dict()))
        self.assertTrue('lastSuccessfulBuild' in data)
        self.assertTrue('lastSuccessfulBuildTime' in data)


    @patch('urllib2.urlopen', Mock(return_value=StringIO("{}")))
    def test_lookup_last_successful_build_returns_none_when_no_build(self):
        # Tests that lookup_last_successful_build() returns None when there is
        # no lastSuccessfulBuild attribute
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        self.assertEqual(job.lookup_last_successful_build(),None)

    @patch('urllib2.urlopen', mock_url_open_last_successful_build)
    def test_lookup_last_successful_build_returns_time_since_build(self):
        # Tests that lookup_last_successful_build() pulls from Jenkins server with
        # host and job names for overall job data (I.E. not a specific job number or
        # the last build) to get lastSuccessfulBuild from json
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        data = job.lookup_last_successful_build()

    def test_parse_jenkins_timestamp_returns_none_when_timestamp_invalid(self):
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        for inputdata in ['', None, 'thisisgarbagedata']:
            self.assertEqual(None, job._parse_jenkins_timestamp(inputdata))

    @patch('urllib2.urlopen', mock_url_open_last_successful_build)
    def test_parse_jenkins_timestamp_returns_datetime_when_timestamp_valid(self):
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        data = job.lookup_last_successful_build()
        resultdate = job._parse_jenkins_timestamp(data.get('lastSuccessfulBuildTime'))
        self.assertIsInstance(resultdate, datetime.datetime)

    def test_get_time_diff_returns_years_if_greater_than_one_year(self):
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        timediff = job._get_time_diff(datetime.datetime.now() - datetime.timedelta(days=(366 * 2)))
        self.assertEqual(timediff, "2 years ago")

    def test_get_time_diff_returns_year_if_one_year(self):
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        timediff = job._get_time_diff(datetime.datetime.now() - datetime.timedelta(days=365))
        self.assertEqual(timediff, "1 year ago")

    def test_get_time_diff_returns_months_if_greater_than_one_month(self):
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        timediff = job._get_time_diff(datetime.datetime.now() - datetime.timedelta(days=62))
        self.assertEqual(timediff, "2 months ago")

    def test_get_time_diff_returns_month_if_one_month(self):
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        timediff = job._get_time_diff(datetime.datetime.now() - datetime.timedelta(days=31))
        self.assertEqual(timediff, "1 month ago")

    def test_get_time_diff_returns_days_if_greater_than_one_day(self):
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        timediff = job._get_time_diff(datetime.datetime.now() - datetime.timedelta(days=2))
        self.assertEqual(timediff, "2 days ago")

    def test_get_time_diff_returns_day_if_one_day(self):
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        timediff = job._get_time_diff(datetime.datetime.now() - datetime.timedelta(days=1))
        self.assertEqual(timediff, "1 day ago")

    def test_get_time_diff_returns_hours_if_greater_than_one_hour(self):
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        timediff = job._get_time_diff(datetime.datetime.now() - datetime.timedelta(hours=2))
        self.assertEqual(timediff, "2 hours ago")

    def test_get_time_diff_returns_hour_if_one_hour(self):
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        timediff = job._get_time_diff(datetime.datetime.now() - datetime.timedelta(hours=1))
        self.assertEqual(timediff, "1 hour ago")

    def test_get_time_diff_returns_minutes_if_greater_than_one_minute(self):
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        timediff = job._get_time_diff(datetime.datetime.now() - datetime.timedelta(minutes=2))
        self.assertEqual(timediff, "2 minutes ago")

    def test_get_time_diff_returns_minute_if_one_minute(self):
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        timediff = job._get_time_diff(datetime.datetime.now() - datetime.timedelta(minutes=1))
        self.assertEqual(timediff, "1 minute ago")

    def test_get_time_diff_returns_less_than_minute_if_less_than_minute(self):
        hostname = 'http://localhost:8080'
        jobname = 'Job1'
        job = jenkins.RetrieveJob(hostname,jobname)
        timediff = job._get_time_diff(datetime.datetime.now() - datetime.timedelta(seconds=30))
        self.assertEqual(timediff, "Less than one minute ago")
               

