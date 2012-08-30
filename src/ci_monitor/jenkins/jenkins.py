import urllib2, StringIO
from urlparse import urlparse
from dateutil import parser
import types
import xml.etree.ElementTree as et
import simplejson
    

class PollCI(object):
    """
        This class enables the application to have access to last build status of multiple jobs on different jenkins installations.
        
        The constructor expected a tuple of strings where each element is a URI to a jenkins' view; that is a view that has been previously
        created on that jenkins server of the jobs the application should display on the front end.
        
        The class then pulls the rss feed of the view (the rssAll feed), and creates a list of jobs, then gets each job's last build status
        from the jenkins json api
        
        TODO:  Add logging for cases when the App is imporperly configured
    """
    
    def __init__(self,ci_hosts_tuple,*args,**kwargs):
        """
            Constructor to initialize the object, expects a tuple of URIs pointing to 1 or more jenkins views on 1 or more servers
            
            @param ci_hosts_tuple tuple
        """
        self.hosts = ci_hosts_tuple
        self.last_build = '/lastBuild/api/json'
    
    def sort_entry_list(self,entry_list,ns):
        """
            Function to sort a list of similar entity elements (the same jenkins job) from the RSS feed by their updated date.
        
            @param entry_list list 
            @param ns string
        """
        if entry_list is None or ns is None:
            #TODO: email admins that config has a problem
            return None
        
        if not type(entry_list) == types.ListType:
            return [entry_list]
        
        if len(entry_list) == 1:
            return entry_list
            
        return sorted(entry_list,key=lambda entry: parser.parse(entry.find('%supdated' % ns).text), reverse=True)
        
    def filter_entries(self, entries,ns):
        """
            Function to organize the list of entry elements into a logical grouping (the same jenkins job),
            then sort each list of like jobs and return a set of jobs ordered by desc updated date.
            
            @param entries list
            @param ns string
        """
        d = dict()
        results = []
        
        if entries is None or ns is None:
            return []
            
        if not type(entries) == types.ListType:
            return [entries]
            
        if len(entries) == 1:
            return entries
            
        for entry in entries:
            job_link = self.get_job_link(entry,ns)
            if not job_link: continue
            
            if job_link in d:
                d[job_link].append(entry)
            else:               
                d[job_link] = [entry]

        for k,v in d.iteritems():
            results.append(self.sort_entry_list(v,ns)[0])
        return results
        
        
    def get_entries(self,conn):
        """
            Function to read the RSS feed and extract all entry elements.  Each entry element is a jenkins build
            
            @param hostname string
            @param ns string
        """
        
        if conn is None: return [],''
        
        try:
            feed = et.parse(conn).getroot()
        except:
            #TODO: email admins that config has a problem
            return [],''
        
        ns = feed.tag.replace('feed','')
        
        entries = feed.findall('%sentry' % ns)
        conn.close()
        return entries,ns
        
    def get_job_name_from_job_link(self,job_link):
        
        if job_link is None:
            return None
            
        if job_link.find('/job') > -1:
            return job_link[job_link.find('/job')+5:len(job_link)]
            
        return None
        
    def get_job_link(self,entry,ns):
        """
            Function to extract the href attribute of the link element in the given entry element.  The href attribute is the URI for a
            jenkins job
            
            @param entry Element
            @param ns string
        """
        if entry is None or ns is None:
            return None
            
        link = entry.find('%slink' % ns)
        return link.get('href').rstrip('/')[0:link.get('href').rstrip('/').rfind('/')]
        
    
        
    def get_job_last_build_status(self, conn,job_link):
        """
            Function to retrieve the last build status from the jenkins json api based on the job's URI
            
            @param job_link string
        """
        if conn is None: return None
        
        json = simplejson.load(conn)
        
        if 'result' in json and 'fullDisplayName' in json:
            job_name = self.get_job_name_from_job_link(job_link) or json.get('fullDisplayName')
            status   = json.get('result')
        else:
            return None
            
        conn.close()
        return dict(
            job_name = job_name,
            status   = status,
        )
        
    def read_rss(self):
        """
            Function to be called by instantiator, to pull the RSS feed for all jenkins views given to the constructor, filter for individual jobs, and sort by DESC updated date,
            and return a list of each job's latest build status as a json list
        """
        results = []
        
        if self.hosts is None:
            return results

        for hostname in self.hosts:
            conn = urllib2.urlopen(hostname)
            entries,ns = self.get_entries(conn)
                
            entries = self.filter_entries(entries,ns)
            
            d = dict(
                hostname = hostname,
                elements = entries
            )
            results.append(d)

        return results,ns
        
    def poll(self, entry, ns):
        if entry is None: return dict()
        
        job_link = self.get_job_link(entry,ns)
        
        if job_link is None: return dict()
        
        conn = urllib2.urlopen('%s/%s' % (job_link,self.last_build))
        json = self.get_job_last_build_status(conn,job_link)
        
        return json or dict()