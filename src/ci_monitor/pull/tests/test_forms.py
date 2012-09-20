"""
CI-Monitor v1.0 A Continous Integration Monitoring Tool

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
from django.utils import unittest

from ci_monitor.pull import views, models

class FormsTests(unittest.TestCase):
    
    def setUp(self):
        self.POST = dict(
            hostname    = 'http://edge-master:8080',
            jobname     = 'bootstrap',
            displayname = 'bootstrap',
            left        = '0px',
            top         = '0px',
            width       = '340px',
            hieght      = '340px',     
            status      = 'SUCCESS'
        )
        
        self.ci_server = models.CiServer(hostname='http://secure.voltage.com')
        self.ci_server.save()
        
        self.ci_server1 = models.CiServer(hostname='http://jenkins.voltate.com')
        self.ci_server1.save()
        
        self.ci_job = models.CiJob(jobname='euphoria', status='SUCCESS')
        self.ci_job.ci_server = self.ci_server1
        self.ci_job.save()
        
        
    def test_save_new_ci_server(self):
        ci_server = views.save_ci_server(**self.POST)
        self.assertEqual(ci_server.hostname, self.POST['hostname'])
        
    def test_save_ci_server_when_server_exists(self):
        ci_server = models.CiServer(hostname='http://voltage.com')
        ci_server.save()
        
        self.POST['hostname'] = 'http://voltage.com'
        actual = views.save_ci_server(**self.POST)
        
        self.assertEqual(actual.hostname,ci_server.hostname)
        
    def test_save_new_ci_job(self):
        self.POST['hostname'] = 'http://secure.voltage.com'
        self.POST['ci_server'] = self.ci_server.pk
        
        ci_job = views.save_ci_job(**self.POST)
        self.assertEqual(ci_job.jobname, self.POST['jobname'])
        self.assertEqual(ci_job.status, self.POST['status'])
        self.POST.pop('ci_server')
        
    def test_save_ci_job_when_ci_job_exists(self):
        self.POST['hostname'] = 'http://jenkins.voltate.com'
        self.POST['jobname'] = 'euphoria'
        self.POST['ci_server'] = self.ci_server1.pk
        
        ci_job = views.save_ci_job(**self.POST)
        self.assertEqual(ci_job.id,self.ci_job.id)
        
        self.POST.pop('ci_server')
        
        
        