import urllib2, StringIO
from urlparse import urlparse
from dateutil import parser
import types
import xml.etree.ElementTree as et
import simplejson

class RetrieveJob(object):
    
    def __init__(self, hostname, jobname):
        self.hostname = hostname
        self.jobname = jobname
        
    def lookup_hostname(self):
        try:
            if self.hostname.find('cloudbees') > -1:
                req = urllib2.Request(self.hostname)
                import base64
                base64string = base64.encodestring('%s:%s' % ('sam.mohamed@voltage.com', 'voltage321'))[:-1]
                authheader =  "Basic %s" % base64string
                req.add_header("Authorization", authheader)
                conn = urllib2.urlopen(req,timeout=5)
            else:
                conn = urllib2.urlopen(self.hostname,timeout=5)
            conn.close()
            return True
        except ValueError:
            return ValueError
        except urllib2.URLError:
            return urllib2.URLError
            
    def lookup_job(self):
        try:
            if self.hostname.find('cloudbees') > -1:
                req = urllib2.Request('%s/job/%s/lastBuild/api/json' % (self.hostname,self.jobname))
                import base64
                base64string = base64.encodestring('%s:%s' % ('sam.mohamed@voltage.com', 'voltage321'))[:-1]
                authheader =  "Basic %s" % base64string
                req.add_header("Authorization", authheader)
                conn = urllib2.urlopen(req,timeout=5)
            else:
                conn = urllib2.urlopen('%s/job/%s/lastBuild/api/json' % (self.hostname,self.jobname),timeout=5)
            
            json = simplejson.load(conn)

            if 'result' in json and 'fullDisplayName' in json:
                jobname = self.jobname
                status   = json.get('result')
            else:
                return None
                
        except ValueError:
            return ValueError
        except urllib2.URLError:
            return urllib2.URLError
            
        conn.close()
        return dict(
            jobname = jobname,
            status   = status,
        )