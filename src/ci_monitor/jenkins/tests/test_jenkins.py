from xml.etree import ElementTree as et
from dateutil import parser

from django.utils import unittest
from django.conf import settings

from ci_monitor.jenkins.jenkins import PollCI

class JenkinsMouleTests(unittest.TestCase):
	
	def setUp(self):
		pass
		
	def test_constructor(self):
		#test a normal constructor
		poll = PollCI(settings.CI_INSTALLATIONS)
		self.assertEquals(type(poll),PollCI)
		
		#test a constructor with null arguments
		poll = PollCI(None)
		self.assertEqual(poll.hosts,None)
		
		#test constructor with extra keyword argument
		poll = PollCI(settings.CI_INSTALLATIONS,test='test')
		self.assertEqual(poll.hosts,settings.CI_INSTALLATIONS)
		
		#test constructor with extra positional arguments
		poll = PollCI(settings.CI_INSTALLATIONS,'one','two')
		self.assertEqual(poll.hosts,settings.CI_INSTALLATIONS)
		
	
	def test_get_job_name(self):
		
		#test normal case, function returned expected job name
		link = 'http://localhost:8080/job/test1'
		expected = 'test1'
		poll = PollCI(settings.CI_INSTALLATIONS)
		
		actual = poll.get_job_name_from_job_link(link)
		self.assertEqual(actual,expected)
		
		#test case when function gets a null parameter
		actual = poll.get_job_name_from_job_link(None)
		self.assertEqual(actual,None)
		
		#test case when function gets an empty string
		actual = poll.get_job_name_from_job_link('')
		self.assertEqual(actual,None)
		
		#test case when function gets a link without the /job part of the string
		actual = poll.get_job_name_from_job_link('http://localhost:8080/test1/1')
		self.assertEqual(actual,None)
		
		
		
		
	def test_sort_list_of_entries(self):
		#test the positive case: function sorts elements as expected
		doc = et.fromstring("""
			<feed xmlns="http://www.w3.org/2005/Atom">
			<entry>
				<title>test1 #1 (broken since this build)</title>
				<link type="text/html" href="http://localhost:8080/job/test1/1/" rel="alternate"/>
				<id>tag:hudson.dev.java.net,2012:test1:2012-08-24_14-10-13</id>
				<published>2012-08-24T21:10:13Z</published>
				<updated>2012-08-24T21:10:13Z</updated>
			</entry>
			<entry>
				<title>test1 #2 (broken for a long time)</title>
				<link type="text/html" href="http://localhost:8080/job/test1/2/" rel="alternate"/>
				<id>tag:hudson.dev.java.net,2012:test1:2012-08-24_14-10-17</id>
				<published>2012-08-24T21:10:17Z</published>
				<updated>2012-08-24T21:10:17Z</updated>
			</entry>
			<entry>
				<title>test1 #2 (broken for a long time)</title>
				<link type="text/html" href="http://localhost:8080/job/test1/2/" rel="alternate"/>
				<id>tag:hudson.dev.java.net,2012:test1:2012-08-24_14-10-17</id>
				<published>2012-08-24T21:10:17Z</published>
				<updated>2012-08-24T20:10:17Z</updated>
			</entry>
			<entry>
				<title>test1 #2 (broken for a long time)</title>
				<link type="text/html" href="http://localhost:8080/job/test1/2/" rel="alternate"/>
				<id>tag:hudson.dev.java.net,2012:test1:2012-08-24_14-10-17</id>
				<published>2012-08-24T21:10:17Z</published>
				<updated>2012-08-24T22:10:17Z</updated>
			</entry>
			</feed>
		""")
		ns = doc.tag.replace('feed','')
		entries = doc.findall('%sentry' % ns)
		expected = [entries[3],entries[1],entries[0],entries[2]]
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual = poll.sort_entry_list(entries,ns)
		self.assertEquals(actual,expected)
		
		#test case when function receives a null list to sort and a null namespace
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual = poll.sort_entry_list(None,None)
		self.assertEqual(actual,None)
					
		#test case when function is given a list with 1 entry
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual = poll.sort_entry_list([entries[0]],ns) 
		expected = [entries[0]]
		self.assertEqual(actual,expected)
		
		#test case when function is not given a list, but given an xml element
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual = poll.sort_entry_list(entries[0],ns) 
		expected = [entries[0]]
		self.assertEqual(actual,expected)
		

	def test_filter_entry_list(self):
		doc = et.fromstring("""
			<feed xmlns="http://www.w3.org/2005/Atom">
			<entry>
				<title>test3 #1 (stable)</title>
				<link type="text/html" href="http://localhost:8080/job/test3/1/" rel="alternate"/>
				<id>tag:hudson.dev.java.net,2012:test3:2012-08-24_14-10-34</id>
				<published>2012-08-24T21:10:34Z</published><updated>2012-08-24T21:10:34Z</updated>
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
		ns = doc.tag.replace('feed','')
		entries = doc.findall('%sentry' % ns)

		poll = PollCI(settings.CI_INSTALLATIONS)
		actual = poll.filter_entries(entries,ns)
	
		test_1 = 3 #expected number of entries after filter
		test_2 = parser.parse('2012-08-24T21:10:17Z') #expected time of entry element of job: test1
		
		actual_1 = len(actual)
		
		for elem in actual:
			if elem[0].text.find('test1') > -1:
				actual_2 = parser.parse(elem[3].text)
				
		self.assertEqual(actual_1,test_1)
		self.assertEqual(actual_2,test_2)	
		
		#test case when function is given a null parameter
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual = poll.filter_entries(None,None)
		self.assertEqual(actual,[])
		
		#test case when function is given an empty list
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual = poll.filter_entries(None,None)
		self.assertEqual(actual,[])
		
		#test case when function is given a single xml Element as a param
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual = poll.filter_entries(entries[0],ns)
		self.assertEqual(len(actual),1)
		import types
		self.assertEqual(type(actual),types.ListType)
		self.assertEqual(actual,[entries[0]])
		
	def test_poll(self):
		doc = et.fromstring("""
			<feed xmlns="http://www.w3.org/2005/Atom">
			<entry>
				<title>test3 #1 (stable)</title>
				<link type="text/html" href="http://localhost:8080/job/test3/1/" rel="alternate"/>
				<id>tag:hudson.dev.java.net,2012:test3:2012-08-24_14-10-34</id>
				<published>2012-08-24T21:10:34Z</published><updated>2012-08-24T21:10:34Z</updated>
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
		expected = [
			dict(
				job_name = "test3",
				status = "SUCCESS"
				),
			dict(
				job_name = "test2",
				status = "SUCCESS"
				),
			dict(
				job_name = "test1",
				status = "FAILURE"
				)
		]
		
		
		#test case when function is given a null param
		poll = PollCI(settings.CI_INSTALLATIONS)
		poll.hosts = None
		actual = poll.poll()
		self.assertEquals(actual,[])
		
		#test when function gets expected result
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual = poll.poll()
		self.assertEqual(len(actual),len(expected))
		
		expected = ["FAILURE","SUCCESS","SUCCESS"]
		actual_result = []
		
		for item in actual:
			for k,v in item.iteritems():
				if k == 'status':
					actual_result.append(v)
				
		self.assertEqual(actual_result,expected)
		
	def test_get_job_link(self):
		doc = et.fromstring("""
			<feed xmlns="http://www.w3.org/2005/Atom">
			<entry>
				<title>test3 #1 (stable)</title>
				<link type="text/html" href="http://localhost:8080/job/test3/1/" rel="alternate"/>
				<id>tag:hudson.dev.java.net,2012:test3:2012-08-24_14-10-34</id>
				<published>2012-08-24T21:10:34Z</published><updated>2012-08-24T21:10:34Z</updated>
			</entry>
			</feed>
		""")
		ns = doc.tag.replace('feed','')
		entry = doc.find('%sentry' % ns)
		
		expected = 'http://localhost:8080/job/test3'
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual = poll.get_job_link(entry,ns)
		
		self.assertEquals(actual,expected)
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual = poll.get_job_link(entry,ns)
		
		#test case when function is given a null param
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual = poll.get_job_link(None,ns)
		self.assertEqual(actual,None)
		
	def test_get_job_last_build_status(self):
		expected = dict(
			job_name = "test3",
			status = "SUCCESS"
		)
		
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual = poll.get_job_last_build_status('http://localhost:8080/job/test3')
		self.assertEquals(actual,expected)
		
		#test case when function is given a null parameter
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual = poll.get_job_last_build_status(None)
		self.assertEquals(actual,None)
		
		#test case when function is given an invalid URI
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual = poll.get_job_last_build_status('localhost:8080/job/test3')
		self.assertEquals(actual,None)	

	def test_get_entries(self):
		#test positive case: function returns 4 entry elements
		doc = et.fromstring("""
			<feed xmlns="http://www.w3.org/2005/Atom">
			<entry>
				<title>test3 #1 (stable)</title>
				<link type="text/html" href="http://localhost:8080/job/test3/1/" rel="alternate"/>
				<id>tag:hudson.dev.java.net,2012:test3:2012-08-24_14-10-34</id>
				<published>2012-08-24T21:10:34Z</published><updated>2012-08-24T21:10:34Z</updated>
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
		ns = doc.tag.replace('feed','')
		expected = doc.findall('%sentry' %ns)
		poll = PollCI(settings.CI_INSTALLATIONS)
		for host in poll.hosts:
			actual,ns1 = poll.get_entries(host)
			self.assertEqual(len(actual),len(expected))
			self.assertEqual(ns1,ns)
			
		#test function when given a null hostname
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual,ns1 = poll.get_entries(None)
		self.assertEqual(len(actual),0)
					
		#test function when given an invalid uri for a view
		poll = PollCI(settings.CI_INSTALLATIONS)
		actual,ns1 = poll.get_entries('localhost:8000/invalid/')
		self.assertEqual(len(actual),0)	
		