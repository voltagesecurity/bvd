from xml.etree import ElementTree as et
from dateutil import parser
import simplejson
from StringIO import StringIO

from django.utils import unittest
from django.conf import settings

from mock import Mock

from ci_monitor.jenkins import jenkins

def mock_url_open_conn_for_rss_feed():
    xml_string = """
          <feed xmlns="http://www.w3.org/2005/Atom"><title>All all builds</title><link type="text/html" href="http://localhost:8080/" rel="alternate"/><updated>2012-08-24T21:10:34Z</updated><author><name>Jenkins Server</name></author><id>urn:uuid:903deee0-7bfa-11db-9fe1-0800200c9a66</id><entry><title>test3 #1 (stable)</title><link type="text/html" href="http://localhost:8080/job/test3/1/" rel="alternate"/><id>tag:hudson.dev.java.net,2012:test3:2012-08-24_14-10-34</id><published>2012-08-24T21:10:34Z</published><updated>2012-08-24T21:10:34Z</updated></entry><entry><title>test2 #1 (stable)</title><link type="text/html" href="http://localhost:8080/job/test2/1/" rel="alternate"/><id>tag:hudson.dev.java.net,2012:test2:2012-08-24_14-10-26</id><published>2012-08-24T21:10:26Z</published><updated>2012-08-24T21:10:26Z</updated></entry><entry><title>test1 #2 (broken for a long time)</title><link type="text/html" href="http://localhost:8080/job/test1/2/" rel="alternate"/><id>tag:hudson.dev.java.net,2012:test1:2012-08-24_14-10-17</id><published>2012-08-24T21:10:17Z</published><updated>2012-08-24T21:10:17Z</updated></entry><entry><title>test1 #1 (broken since this build)</title><link type="text/html" href="http://localhost:8080/job/test1/1/" rel="alternate"/><id>tag:hudson.dev.java.net,2012:test1:2012-08-24_14-10-13</id><published>2012-08-24T21:10:13Z</published><updated>2012-08-24T21:10:13Z</updated></entry></feed>
    """
    return StringIO(xml_string)
    
def mock_url_open_job_last_build():
    json_str = """
            {"actions":[{"causes":[{"shortDescription":"Started by user anonymous","userId":null,"userName":"anonymous"}]}],"artifacts":[],"building":false,"description":null,"duration":54,"estimatedDuration":54,
            "fullDisplayName":"test3#1",
            "id":"2012-08-24_14-10-34","keepLog":false,"number":1,"result":"SUCCESS","timestamp":1345842634000,
            "url":"http://localhost:8080/job/test3/1/","builtOn":"","changeSet":{"items":[],"kind":null},"culprits":[]}
            """
    return StringIO(json_str)

    
def generate_xml_doc():
    doc = et.fromstring("""
        <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <title>test3 #1 (stable)</title>
            <link type="text/html" href="http://localhost:8080/job/test3/1/" rel="alternate"/>
            <id>tag:hudson.dev.java.net,2012:test3:2012-08-24_14-10-34</id>
            <published>2012-08-24T21:10:34Z</published>
            <updated>2012-08-24T21:10:34Z</updated>
        </entry>
        <entry>
            <title>test2 #1 (stable)</title>
            <link type="text/html" href="http://localhost:8080/job/test2/1/" rel="alternate"/>
            <id>tag:hudson.dev.java.net,2012:test2:2012-08-24_14-10-26</id>
            <published>2012-08-24T21:10:26Z</published>
            <updated>2012-08-24T21:10:26Z</updated>
        </entry>
        <entry>
            <title>test1 #2 (broken for a long time)</title>
            <link type="text/html" href="http://localhost:8080/job/test1/2/" rel="alternate"/>
            <id>tag:hudson.dev.java.net,2012:test1:2012-08-24_14-10-17</id>
            <published>2012-08-24T21:10:17Z</published>
            <updated>2012-08-24T21:10:17Z</updated>
        </entry>
        <entry>
            <title>test1 #1 (broken since this build)</title>
            <link type="text/html" href="http://localhost:8080/job/test1/1/" rel="alternate"/>
            <id>tag:hudson.dev.java.net,2012:test1:2012-08-24_14-10-13</id>
            <published>2012-08-24T21:10:13Z</published>
            <updated>2012-08-24T21:10:13Z</updated>
        </entry>
        </feed>
    """)
    return doc

class JenkinsMouleTests(unittest.TestCase):
        
    def test_constructor_with_valid_argument(self):
        #test a normal constructor
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        self.assertEquals(type(poll),jenkins.PollCI)
        
    def test_constructor_with_null_argument(self):
        #test a constructor with null arguments
        poll = jenkins.PollCI(None)
        self.assertEqual(poll.hosts,None)
        
    def test_constructor_with_extra_keyword_argument(self):
        #test constructor with extra keyword argument
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS,test='test')
        self.assertEqual(poll.hosts,settings.CI_INSTALLATIONS)
        
    def test_constructor_with_extra_positional_argument(self):
        #test constructor with extra positional arguments
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS,'one','two')
        self.assertEqual(poll.hosts,settings.CI_INSTALLATIONS)
        

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
        poll.hosts = None
        actual = poll.read_rss()
        self.assertEquals(actual,[])
        io.truncate()
        
    def test_expected_read_rss_feeds(self):
        doc = generate_xml_doc()
        ns = doc.tag.replace('feed','')
        elements = doc.findall('%sentry' % ns)
        elements = elements[:-1]

        expected = ([dict(
            hostname = settings.CI_INSTALLATIONS[0],
            elements = elements,
                    )],
                    ns)
        io = mock_url_open_conn_for_rss_feed()
        io.seek(0)
        jenkins.urllib2.urlopen = Mock(return_value=io)
        poll = jenkins.PollCI(settings.CI_INSTALLATIONS)
        actual = poll.read_rss()
        self.assertEquals(len(actual[0][0].values()),len(expected[0][0].values()))
        
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
        self.assertEquals(actual,dict())