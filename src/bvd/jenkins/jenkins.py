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