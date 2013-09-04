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
from dateutil import parser, relativedelta
import datetime
import types
import xml.etree.ElementTree as et
import simplejson
import re

class RetrieveJob(object):
    
    def __init__(self, hostname, jobname):
        self.hostname = hostname
        self.jobname = jobname

    def _parse_jenkins_timestamp(self, timestamp):
        """
            Parses the timestamp returned from Jenkins' JSON api and returns a python datetime object
        """
        expression = re.compile(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}')
        if not timestamp or not expression.match(timestamp):
            return None
        date = parser.parse(timestamp[:10] + ' ' + timestamp[11:].replace('-',':'))
        return date

    def _get_time_diff(self, time):
        """
            Returns a human-readable difference in time between the given timestamp and the present time
        """
        if isinstance(time, datetime.datetime):
            diff = relativedelta.relativedelta(datetime.datetime.now(),time)
            if diff.years >=1:
                if diff.years > 1:
                    return str(diff.years) + " years ago"
                else:
                    return "1 year ago"
            elif diff.months >= 1:
                if diff.months > 1:
                    return str(diff.months) + " months ago"
                else:
                    return "1 month ago"
            elif diff.days >= 1:
                if diff.days > 1:
                    return str(diff.days) + " days ago"
                else:
                    return "1 day ago"
            elif diff.hours >= 1:
                if diff.hours > 1:
                    return str(diff.hours) + " hours ago"
                else:
                    return "1 hour ago"
            elif diff.minutes >= 1 :
                if diff.minutes > 1:
                     return str(diff.minutes) + " minutes ago"
                else:
                    return "1 minute ago"
            else:
                return "Less than one minute ago"

        else:
            return None

    def lookup_hostname(self, use_auth=False, username=None, password=None):
        """
            Determines if the given hostname is accessible by BVD
        """
        try:
            if use_auth:
                req = urllib2.Request(self.hostname)
                import base64
                base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
                authheader =  "Basic %s" % base64string
                req.add_header("Authorization", authheader)
                conn = urllib2.urlopen(req,timeout=5)
            else:
                conn = urllib2.urlopen(self.hostname,timeout=5)
            conn.close()
            return True
        except ValueError:
            return ValueError
        except urllib2.HTTPError, e:
            print '>>>>>>>>>>>>>', e.code
            #check the status code
            if e.code == 403: #requires authentication
                return 403
            elif e.code == 401: #invalid credentials
                return 401
            return urllib2.URLError
        except urllib2.URLError:
            return urllib2.URLError
        
            
    def lookup_job(self, use_auth=False, username=None, password=None):
        """
            Determines if the given job can be found and returns the status of the job
        """
        try:
            if use_auth:
                # Create auth header for request
                import base64
                base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
                authheader =  "Basic %s" % base64string

                # Create request and add auth header
                req = urllib2.Request('%s/job/%s/lastBuild/api/json' % (self.hostname,self.jobname))
                req.add_header("Authorization", authheader)
                conn = urllib2.urlopen(req,timeout=5)
            else:
                # Request job without auth
                conn = urllib2.urlopen('%s/job/%s/lastBuild/api/json' % (self.hostname,self.jobname),timeout=5)
            
            json = simplejson.load(conn)
            conn.close()
                
        except ValueError:
            return ValueError

        except urllib2.HTTPError, e:
            #check the status code
            if e.code == 403: #requires authentication
                return urllib2.HTTPError
            return urllib2.URLError

        except urllib2.URLError:
            return urllib2.URLError

        if 'result' in json and 'fullDisplayName' in json:
            jobname = self.jobname
            status   = json.get('result')
        else:
            return None
        
        return dict(
            jobname = jobname,
            status   = status,
        )

    def lookup_last_successful_build(self, use_auth=False, username=None, password=None):
        """
            Looks up the last successful build of the given job and returns data on the timestamp
        """
        # Lookup lastSuccessfulBuild number
        try:
            if use_auth:
                # Create auth header for request
                import base64
                base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
                authheader =  "Basic %s" % base64string

                # Create request for general job info
                req_general = urllib2.Request('%s/job/%s/api/json' % (self.hostname,self.jobname))
                req_general.add_header("Authorization", authheader)
                conn_general = urllib2.urlopen(req_general,timeout=5)
            else:
                # Request general job info without auth
                conn_general = urllib2.urlopen('%s/job/%s/api/json' % (self.hostname,self.jobname))

        except ValueError:
            return ValueError

        except urllib2.HTTPError, e:
            #check the status code
            if e.code == 403: #requires authentication
                return urllib2.HTTPError
            return urllib2.URLError

        except urllib2.URLError:
            return urllib2.URLError

        json_general = simplejson.load(conn_general)
        conn_general.close()

        if 'lastSuccessfulBuild' in json_general:
            lastSuccessfulBuild = json_general.get('lastSuccessfulBuild').get('number')
        else:
            return None

        # lookup timestamp of last successful build
        try:
            if use_auth:
                # Create auth header for request
                import base64
                base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
                authheader =  "Basic %s" % base64string

                # Create request for general job info
                req_specific = urllib2.Request('%s/job/%s/%d/api/json' % (self.hostname,self.jobname, lastSuccessfulBuild))
                req_specific.add_header("Authorization", authheader)
                conn_specific = urllib2.urlopen(req_specific,timeout=5)
            else:
                # Request general job info without auth
                conn_specific = urllib2.urlopen('%s/job/%s/%d/api/json' % (self.hostname,self.jobname, lastSuccessfulBuild))

        except ValueError:
            return ValueError

        except urllib2.HTTPError, e:
            #check the status code
            if e.code == 403: #requires authentication
                return urllib2.HTTPError
            return urllib2.URLError

        except urllib2.URLError:
            return urllib2.URLError

        json_specific = simplejson.load(conn_specific)
        conn_specific.close()

        if 'id' in json_specific:
            lastSuccessfulBuildTime = json_specific.get('id')
        else:
            return None

        time = self._parse_jenkins_timestamp(lastSuccessfulBuildTime)
        timesince = self._get_time_diff(time)

        return dict(
            lastSuccessfulBuild = lastSuccessfulBuild,
            lastSuccessfulBuildTime = lastSuccessfulBuildTime,
            timeSinceLastSuccess = timesince
        )

