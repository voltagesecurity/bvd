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
from django import forms
from django.conf import settings
from django.contrib.auth.models import User

from bvd.pull import models


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','username',)
        
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    
    def clean_username(self):
        try:
            user = User.objects.get(username=self.cleaned_data.get('username'))
            raise forms.ValidationError('User exists')
        except User.DoesNotExist:
            pass
        return self.cleaned_data['username']
    
    def save(self):
        user = super(SignupForm,self).save(commit=False)
        if self.cleaned_data.get('password1',None):
            user.set_password(self.cleaned_data.get('password1'))
        user.save()
        
class CiServerForm(forms.ModelForm):
    
    class Meta:
        model = models.CiServer
        
class UserCiJobForm(forms.ModelForm):
    
    class Meta:
        model = models.UserCiJob
        fields = ('user', 'ci_server', 'jobname', 'status', 'displayname', 'icon', 'width',
            'height', 'readonly', 'entity_active', 'appletv', 'appletv_active')
