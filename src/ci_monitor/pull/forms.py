from django import forms
from django.contrib.auth.models import User

from ci_monitor.pull import models

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
        
class SaveUserJobForm(forms.Form):
    
    hostname = forms.CharField()
    jobname = forms.CharField()
    displayname = forms.CharField()
    top = forms.CharField()
    left = forms.CharField()
    width = forms.CharField()
    height = forms.CharField()
    status = forms.CharField()
    
    def __init__(self,request,*args,**kwargs):
        super(SaveUserJobForm,self).__init__(*args,**kwargs)
        self.request = request
    
    def save(self):
        try:
            job = models.CiJob.objects.get(jobname=jobname,ci_server__hostname=hostname,entity_active=True)
            job.left_position = left
            job.top_position = top
            job.width = width
            job.height = height
            job.status = status
            job.save()
        except models.CjJob.DoesNotExist:
            job = models.CiJob(jobname=jobname, left_position=left, top_position=top, entity_active=True, status=status, displayname=displayname, width=width, height=height)
            job.ci_server = server
            job.save()
            
        try:
            user_job = models.UserCiJob.get(user__username=self.request.user.username,ci_job__jobname=job.jobname)
        except models.UserCiJob.DoesNotExist:
            user_job = models.UserCiJob()
            user_job.user = self.request.user
            user_job.ci_job = job
            user_job.save()
            
        