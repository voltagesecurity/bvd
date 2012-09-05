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
        self.assertEqual(job.lookup_job(),dict(jobname='test3#1',status='SUCCESS'))
    
"""
class JenkinsMouleTests(unittest.TestCase):
    
        
    def test_constructor_with_valid_argument(self):
        #test a normal constructor
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        self.assertEquals(type(poll),jenkins.PollCI)
        
    def test_constructor_with_null_argument(self):
        #test a constructor with null arguments
        poll = jenkins.PollCI(None)
        self.assertEqual(poll.host,None)
        
    def test_constructor_with_extra_keyword_argument(self):
        #test constructor with extra keyword argument
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS,test='test')
        self.assertEqual(poll.host,settings.CI_INSTALLATIONS)
        
    def test_constructor_with_extra_positional_argument(self):
        #test constructor with extra positional arguments
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS,'one','two')
        self.assertEqual(poll.host,settings.CI_INSTALLATIONS)
        

    def test_get_four_entry_elements(self):
        #test positive case: function returns 4 entry elements
        doc = generate_xml_doc()
        ns = doc.tag.replace('feed','')
        expected = doc.findall('%sentry' %ns)
        io = mock_url_open_conn_for_rss_feed()
        jenkins.urllib2.urlopen = Mock(return_value=io)
        conn = jenkins.urllib2.urlopen(settings.CI_INSTALLATIONS[0])
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual,ns1 = poll.get_entries(conn)
        self.assertEqual(len(actual),len(expected))
        self.assertEqual(ns1,ns)
            
    def test_get_entries_called_with_null_hostname(self):
        #test function when given a null hostname
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual,ns1 = poll.get_entries(None)
        self.assertEqual(actual,[]) 

    def test_get_expected_job_name(self):
        #test normal case, function returned expected job name
        link = 'http://localhost:8080/job/test1'
        expected = 'test1'
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.get_job_name_from_job_link(link)
        self.assertEqual(actual,expected)

    def test_get_job_name_with_null_parameter(self):
        #test case when function gets a null parameter
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.get_job_name_from_job_link(None)
        self.assertEqual(actual,None)

    def test_get_job_name_with_emptry_string_parameter(self):
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        #test case when function gets an empty string
        actual = poll.get_job_name_from_job_link('')
        self.assertEqual(actual,None)

    def test_get_job_name_with_invalid_parameter(self):
        #test case when function gets a link without the /job part of the string
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.get_job_name_from_job_link('http://localhost:8080/test1/1')
        self.assertEqual(actual,None)

    def test_expected_sort_list_of_entries(self):
        #test the positive case: function sorts elements as expected
        doc = generate_xml_doc()
        ns = doc.tag.replace('feed','')
        entries = doc.findall('%sentry' % ns)
        expected = [entries[0],entries[1],entries[2],entries[3]]
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.sort_entry_list(entries,ns)
        self.assertEquals(actual,expected)

    def test_sort_list_of_entries_with_null_paramter(self):
        #test case when function receives a null list to sort and a null namespace
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.sort_entry_list(None,None)
        self.assertEqual(actual,None)

    def test_sort_list_of_entries_when_one_entry_is_given(self):
        #test case when function is given a list with 1 entry
        doc = generate_xml_doc()
        ns = doc.tag.replace('feed','')
        entries = doc.findall('%sentry' % ns)
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.sort_entry_list([entries[0]],ns) 
        expected = [entries[0]]
        self.assertEqual(actual,expected)

    def test_sort_list_of_entries_when_xml_element_is_given(self):
        #test case when function is not given a list, but given an xml element
        doc = generate_xml_doc()
        ns = doc.tag.replace('feed','')
        entries = doc.findall('%sentry' % ns)
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.sort_entry_list(entries[0],ns) 
        expected = [entries[0]]
        self.assertEqual(actual,expected)

    def test_expected_filter_entry_list(self):
        doc = generate_xml_doc()
        ns = doc.tag.replace('feed','')
        entries = doc.findall('%sentry' % ns)

        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.filter_entries(entries,ns)

        test_1 = 3 #expected number of entries after filter
        test_2 = parser.parse('2012-08-24T21:10:17Z') #expected time of entry element of job: test1

        actual_1 = len(actual)

        for elem in actual:
            if elem[0].text.find('test1') > -1:
                actual_2 = parser.parse(elem[3].text)

        self.assertEqual(actual_1,test_1)
        self.assertEqual(actual_2,test_2)
    
    def test_filter_entry_list_with_null_parameter(self):  
        #test case when function is given a null parameter
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.filter_entries(None,None)
        self.assertEqual(actual,[])
    
    def test_filter_entry_list_with_empty_list_parameter(self):
        #test case when function is given an empty list
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.filter_entries(None,None)
        self.assertEqual(actual,[])
        
    def test_filter_entry_list_with_single_xml_element_as_param(self):
        #test case when function is given a single xml Element as a param
        doc = generate_xml_doc()
        ns = doc.tag.replace('feed','')
        entries = doc.findall('%sentry' % ns)
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.filter_entries(entries[0],ns)
        self.assertEqual(len(actual),1)
        import types
        self.assertEqual(type(actual),types.ListType)
        self.assertEqual(actual,[entries[0]])
        
    def test_expected_get_job_link(self):
        doc = generate_xml_doc()
        ns = doc.tag.replace('feed','')
        entry = doc.find('%sentry' % ns)
        expected = 'http://localhost:8080/job/test3'
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.get_job_link(entry,ns)
        self.assertEquals(actual,expected)
    
    def test_get_job_link_with_null_param(self):
        #test case when function is given a null param
        doc = generate_xml_doc()
        ns = doc.tag.replace('feed','')
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.get_job_link(None,ns)
        self.assertEqual(actual,None)
        
    def test_get_expected_job_last_build_status(self):

        expected = dict(
            job_name = "test3",
            status = "SUCCESS"
        )
        io = mock_url_open_job_last_build()
        io.seek(0)
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        jenkins.urllib2.urlopen = Mock(return_value=io)
        conn = jenkins.urllib2.urlopen('http://localhost:8080/job/test3/lastBuild/api/json')
        actual = poll.get_job_last_build_status(conn,'http://localhost:8080/job/test3')
        self.assertEquals(actual,expected)

    def test_get_job_last_build_status_with_null_parameter(self):
        #test case when function is given a null parameter
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.get_job_last_build_status(None,'http://localhost:8080/job/test3')
        self.assertEquals(actual,None)
        
    def test_read_rss_feeds_when_hosts_are_null(self):
        #test case when function is given a null param
        io = mock_url_open_conn_for_rss_feed()
        jenkins.urllib2.urlopen = Mock(return_value=io)
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        poll.host = None
        actual,ns = poll.read_rss()
        self.assertEquals(actual,None)
        self.assertEqual(ns,None)
        
    def test_expected_read_rss_feeds(self):
        doc = generate_xml_doc()
        ns = doc.tag.replace('feed','')
        elements = doc.findall('%sentry' % ns)
        elements = elements[:-1]

        expected = (dict(
            hostname = settings.CI_INSTALLATIONS[0],
            elements = elements,
                    ),
                    ns)
        io = mock_url_open_conn_for_rss_feed()
        jenkins.urllib2.urlopen = Mock(return_value=io)
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.read_rss()
        self.assertEquals(len(actual[0].values()),len(expected[0].values()))
        
    def test_read_rss_with_url_error(self):
        io = mock_url_open_conn_for_rss_feed()
        jenkins.urllib2.urlopen = Mock(return_value=io,side_effect=urllib2.URLError('bad url'))
        expected,ns = jenkins.PollCI(settings.CI_INSTALLATIONS).read_rss()
        self.assertEqual(expected,None)
        self.assertEqual(type(ns),type(urllib2.URLError))
        
    def test_read_rss_with_http_error(self):
        io = mock_url_open_conn_for_rss_feed()
        jenkins.urllib2.urlopen = Mock(return_value=io,side_effect=urllib2.HTTPError('bad url',None,None,None,None))
        expected,ns = jenkins.PollCI(settings.CI_INSTALLATIONS).read_rss()
        self.assertEqual(expected,None)
        self.assertEqual(type(ns),type(urllib2.URLError))
        
    def test_poll_with_expected_result(self):
        #test when function gets expected result
        io = mock_url_open_job_last_build()
        jenkins.urllib2.urlopen = Mock(return_value=io)
        doc = generate_xml_doc()
        
        expected = dict(
                job_name = "test3",
                status = "SUCCESS"
                )
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        ns = doc.tag.replace('feed','')
        actual = poll.poll(doc.findall('%sentry' % ns)[0], ns)
        self.assertEqual(actual,expected)
        
    
    def test_poll_with_null_parameter(self):
        #test case when function is given a null param
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.poll(None,None)
        self.assertEquals(actual,None)
        
    def test_filter_entries_with_matrix_jobs_returned_expected(self):
        doc = generate_xml_doc_with_matrix()
        ns = doc.tag.replace('feed','')
        entries = doc.findall('%sentry' % ns)
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.filter_entries(entries,ns)
        self.assertEqual(len(actual),4)
        import types
        self.assertEqual(type(actual),types.ListType)
        
    def test_get_job_link_link_of_matrix_job(self):
        doc = generate_xml_doc_with_matrix()
        ns = doc.tag.replace('feed','')
        entries = doc.findall('%sentry' % ns)
        entry = entries[-2]
        expected = None
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.get_job_link(entry,ns)
        self.assertEqual(actual,expected)
"""