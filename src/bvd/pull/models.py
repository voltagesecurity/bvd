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
from django.db import models
from django.contrib.auth.models import User

class CiServer(models.Model):
    
    hostname = models.CharField(max_length=200,primary_key=True)
    
    def __unicode__(self):
        return self.hostname
    
class UserCiJob(models.Model):
    user = models.ForeignKey(User)
    ci_server = models.ForeignKey('CiServer')
    jobname = models.CharField(max_length=100)
    status = models.CharField(max_length=10,null=True,blank=True)
    displayname = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, null=True, blank=True)
    width = models.CharField(max_length=10,null=True,blank=True)
    height = models.CharField(max_length=10,null=True,blank=True)
    readonly = models.NullBooleanField(null=True,blank=True)
    entity_active = models.BooleanField()
    
    def __unicode__(self):
        return self.displayname