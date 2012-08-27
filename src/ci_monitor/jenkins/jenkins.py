import urllib2, StringIO
from urlparse import urlparse
from dateutil import parser
import xml.etree.ElementTree as et
from django.utils import simplejson

class PollCI(object):
	
	def __init__(self,ci_hosts_tuple,*args,**kwargs):
		self.hosts = ci_hosts_tuple
		self.last_build = '/lastBuild/api/json'
	
	def sort_entry_list(self,entry_list,ns):
		return sorted(entry_list,key=lambda entry: parser.parse(entry.find('%supdated' % ns).text), reverse=True)
		
	def filter_entries(self,entries,ns):
		d = dict()
		results = []
		for entry in entries:
			job_link = self.get_job_link(entry,ns)
			if job_link in d:
				d[job_link].append(entry)
			else:				
				d[job_link] = [entry]

		for k,v in d.iteritems():
			if len(v) == 1:
				results.append(v)
			else:
				results.append(self.sort_entry_list(v,ns)[0])
		return results
		
		
	def get_entries(self,hostname,ns):
		conn = urllib2.urlopen(hostname)
		xml_string = StringIO.StringIO(conn.read())
		
		feed = et.parse(xml_string).getroot()
		
		entries = feed.findall('%sentry' % ns)
		conn.close()
		return entries,ns
		
	def get_job_link(self,entry,ns):
		link = entry.find('%slink' % ns)
		return link.get('href').rstrip('/')[0:link.get('href').rstrip('/').rfind('/')]
		
	def get_job_last_build_status(self,job_link):
		conn = urllib2.urlopen('%s/%s'%(job_link,self.last_build))
		
		json = simplejson.load(conn)
		
		if 'result' in json and 'fullDisplayName' in json:
			job_name = json.get('fullDisplayName')
			status   = json.get('result')
			
		conn.close()
		return dict(
			job_name = job_name,
			status   = status,
		)
		
	def poll(self):
		results = []
		for hostname in self.hosts:
			
			entries,ns = self.get_entries(hostname)
			entries = self.filter_entries(entries,ns)
			for entry in entries:
				job_link = self.get_job_link(entry,ns)
				json = self.get_job_last_build_status(job_link)
				results.append(json)
		return results