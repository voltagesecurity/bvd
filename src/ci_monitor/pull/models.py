from django.db import models
from django.contrib.auth.models import User

class CiServer(models.Model):
    
    hostname = models.CharField(max_length=200,primary_key=True)
    
    def __unicode__(self):
        return self.hostname
    
class CiJob(models.Model):
    
    ci_server = models.ForeignKey('CiServer')
    jobname = models.CharField(max_length=100)
    status = models.CharField(max_length=10,null=True,blank=True)
    
    def __unicode__(self):
        return self.jobname
    
class UserCiJob(models.Model):
    user = models.ForeignKey(User)
    ci_job = models.ForeignKey('CiJob')
    displayname = models.CharField(max_length=100)
    left = models.CharField(max_length=10,null=True,blank=True)
    top = models.CharField(max_length=10,null=True,blank=True)
    width = models.CharField(max_length=10,null=True,blank=True)
    height = models.CharField(max_length=10,null=True,blank=True)
    entity_active = models.BooleanField()
    
    def __unicode__(self):
        return self.displayname