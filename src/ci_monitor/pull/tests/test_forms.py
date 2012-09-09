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
        
        
        