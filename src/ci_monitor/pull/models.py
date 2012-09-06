from django.db import models

class CiServer(models.Model):
    
    hostname = models.CharField(max_length=200,primary_key=True)
    
class CiJob(models.Model):
    
    ci_server = models.ForeignKey('CiServer')
    jobname = models.CharField(max_length=100)
    displayname = models.CharField(max_length=100)
    left_position = models.CharField(max_length=5,null=True,blank=True)
    top_position = models.CharField(max_length=5,null=True,blank=True)
    width = models.CharField(max_length=10)
    height = models.CharField(max_length=10)
    status = models.CharField(max_length=10,null=True,blank=True)
    entity_active = models.BooleanField()