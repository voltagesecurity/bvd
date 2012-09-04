from StringIO import StringIO
from xml.etree import ElementTree as et

from django.test.simple import DjangoTestSuiteRunner

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
    
def generate_xml_doc_with_matrix():
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
        <entry>
        	<title>build-vsdataweb-package  pkg_darwin64 #110 (stable)</title>
        	<link type="text/html" href="http://edge-master.voltage.com:8080/job/build-vsdataweb-package/./label=pkg_darwin64/110/" rel="alternate"/>
        	<id>tag:hudson.dev.java.net,2012:label=pkg_darwin64:2012-08-31_18-46-44</id>
        	<published>2012-09-01T01:46:44Z</published>
        	<updated>2012-09-01T01:46:44Z</updated>
        </entry>
        <entry>
        	<title>build-vsdataweb-package #110 (stable)</title>
        	<link type="text/html" href="http://edge-master.voltage.com:8080/job/build-vsdataweb-package/110/" rel="alternate"/>
        	<id>tag:hudson.dev.java.net,2012:build-vsdataweb-package:2012-08-31_18-46-44</id>
        	<published>2012-09-01T01:46:44Z</published>
        	<updated>2012-09-01T01:46:44Z</updated>
        </entry>
        </feed>
    """)
    return doc

    
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

class NoDbTestRunner(DjangoTestSuiteRunner):
	""" A test runner to test without database creation """

	def setup_databases(self, **kwargs):
		""" Override the database creation defined in parent class """
		pass

	def teardown_databases(self, old_config, **kwargs):
		""" Override the database teardown defined in parent class """
		pass