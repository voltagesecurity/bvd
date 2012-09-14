import urllib2, types

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.core import serializers


from ci_monitor.jenkins.jenkins import RetrieveJob
from ci_monitor.pull import models, forms

def append_http(hostname):
    if not hostname: return 'http://'
    
    if hostname.find('http') > -1 or hostname.find('https') > -1:
        return hostname
    else:
        return 'http://%s' % hostname
    
def get_jobs_for_user(user):
    jobs =  models.UserCiJob.objects.filter(entity_active=True,user__username=user.username)
    list = []
    for job in jobs:
        d = dict(
            pk      = job.pk,
            hostname = job.ci_job.ci_server.hostname,
            jobname = job.ci_job.jobname,
            displayname = job.displayname,
            left = job.left,
            top = job.top,
            width = job.width,
            height = job.height,
            status = job.ci_job.status,
                
        )
        list.append(d)
        
    return list

def save_ci_server(**widget):
    try:
        ci_server = models.CiServer.objects.get(hostname=append_http(widget['hostname']))
    except models.CiServer.DoesNotExist:
        ci_server = forms.CiServerForm(data=widget).save()
    
    return ci_server

def save_ci_job(**widget):
    try:
        ci_job =  models.CiJob.objects.get(ci_server__hostname=widget['ci_server'],jobname=widget['jobname'])
    except models.CiJob.DoesNotExist:
        ci_job = forms.CiJobForm(data=widget).save()
        
    return ci_job
    
def save_user_ci_job(**widget):
    ci_server = save_ci_server(**widget)
    widget['ci_server'] = ci_server.pk
    ci_job = save_ci_job(**widget)
    widget['ci_job'] = ci_job.pk
    
    try:
        user_ci_job = models.UserCiJob.objects.get(user__pk=widget['user'], ci_job__jobname=ci_job.jobname)
        form = forms.UserCiJobForm(data=widget,instance=user_ci_job)
        if form.is_valid():
            user_ci_job = form.save()
    except models.UserCiJob.DoesNotExist:
        form = forms.UserCiJobForm(data=widget)
        if form.is_valid():
            user_ci_job = form.save()
    return user_ci_job 
    
def redirect_to_home(request):
    return HttpResponseRedirect('/')

def home(request,template='index.html'):
    if not request.user.is_authenticated():
        jobs = []
        pass
    else:
        jobs = models.UserCiJob.objects.filter(entity_active=True,user__username=request.user.username)
    #jobs = models.CiJob.objects.filter(entity_active=True)
    return render_to_response(template,
                              dict(title='Welcome to CI-Monitor',jobs = jobs),
                              context_instance=RequestContext(request))
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password1')
    
    user = authenticate(username=username,password=password)
    if user and user.is_active:
        django_login(request,user)
        list = get_jobs_for_user(request.user)
        
        return HttpResponse(simplejson.dumps([dict(status = 200, jobs = list)]), content_type = 'application/javascript; charset=utf8')
    
    return HttpResponse(simplejson.dumps([dict(status = 500)]), content_type = 'application/javascript; charset=utf8')

def logout(request):
    django_logout(request)
    return HttpResponse(simplejson.dumps([dict(status = 200)]), content_type = 'application/javascript; charset=utf8')
            
def validate_username(request):
    username = request.POST.get('username')
    
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse(simplejson.dumps([dict(status = 200)]), content_type = 'application/javascript; charset=utf8')

    return HttpResponse(simplejson.dumps([dict(status = 500)]), content_type = 'application/javascript; charset=utf8')
 
def validate_hostname(request):
    job = RetrieveJob(append_http(request.POST.get('hostname',None)),None)
    test = job.lookup_hostname()
    
    if test == urllib2.URLError:
        result = dict(status = 500)
    elif test == ValueError:
        result = dict(status = 404)
    else:
        result = dict(status = 200)
    
    return HttpResponse(simplejson.dumps([result]), content_type = 'application/javascript; charset=utf8')
    
def validate_job(request):
    hostname = append_http(request.POST.get('hostname',''))
    jobname = request.POST.get('jobname',None)
    
    if hostname.strip() == 'http://' or not jobname:
        result = dict(status = 500)
        return HttpResponse(simplejson.dumps([result]), content_type = 'application/javascript; charset=utf8')
        
    job = RetrieveJob(hostname,jobname)
    result = job.lookup_job()
    
    if result == urllib2.URLError:
        result = dict(status = 500)
        return HttpResponse(simplejson.dumps([result]), content_type = 'application/javascript; charset=utf8')
    elif result == ValueError:
        result = dict(status = 404)
        return HttpResponse(simplejson.dumps([result]), content_type = 'application/javascript; charset=utf8')
    else:
        result.update(dict(hostname = hostname))
        
    key = str('%s/%s' % (hostname, jobname))
    
    request.session[key] = result
    return HttpResponse(simplejson.dumps([dict(status = 200)]), content_type = 'application/javascript; charset=utf8')
    
def retrieve_job(request):
    
    if not request.user.is_authenticated():
        result = [dict(status = 401)]
        return HttpResponse(simplejson.dumps(result), content_type = 'application/javascript; charset=utf8')
    
    hostname = append_http(request.POST.get('hostname',''))
    jobname = request.POST.get('jobname',None)
    displayname = request.POST.get('displayname')
    
    if hostname.strip() == 'http://' or not jobname:
        result = [dict(status = 500)]
        return HttpResponse(simplejson.dumps(result), content_type = 'application/javascript; charset=utf8')
    
    key = str('%s/%s' % (hostname, jobname))
    result = request.session[key]
    
    if not result:
        result = dict(status = 500)
        return HttpResponse(simplejson.dumps([result]), content_type = 'application/javascript; charset=utf8')
    
    #check to see if the user has already added the job
    user_ci_job = models.UserCiJob.objects.filter(entity_active=True,ci_job__jobname=jobname,user__username=request.user.username)
    if len(user_ci_job) > 0:
        result = dict(status = 100)
        return HttpResponse(simplejson.dumps([result]), content_type = 'application/javascript; charset=utf8')
    
    widget = dict(
         hostname = hostname,
         jobname = jobname,
         displayname = displayname,
         status = result['status'],
         user = request.user.pk,
         entity_active = True,
     )
    user_ci_job = save_user_ci_job(**widget)
    result.update(dict(displayname = displayname, jobname = jobname, pk = user_ci_job.pk))
        
    return HttpResponse(simplejson.dumps([result]), content_type = 'application/javascript; charset=utf8')



def save_jobs(request):
    if not request.user.is_authenticated():
        result = [dict(status = 401)]
        return HttpResponse(simplejson.dumps(result), content_type = 'application/javascript; charset=utf8')
    
    user = request.user
    widgets = simplejson.loads(request.POST['widgets'])
    
    if not widgets:
        result = [dict(status = 500)]
        return HttpResponse(simplejson.dumps(result), content_type = 'application/javascript; charset=utf8')
    
    for widget in widgets:
        widget['user'] = user.pk
        widget['entity_active'] = True
        save_user_ci_job(**widget)
    result = [dict(status = 200)]
    return HttpResponse(simplejson.dumps(result), content_type = 'application/javascript; charset=utf8')
    
def autocomplete_hostname(request):
    txt = request.POST.get('txt')
    servers = models.CiServer.objects.filter(hostname__icontains=txt)
    result = [server.hostname for server in servers]
    #result = ['http://localhost:80%d' % i for i in range(5)]
    return HttpResponse(simplejson.dumps(result), content_type = 'application/javascript; charset=utf8')
    
    
def get_modal(request):
    template = request.GET.get('template') 
    if template == 'add_job':
        if not request.user.is_authenticated():
            template = 'login_required.html'
            return render_to_response(template,
                  dict(),
                  context_instance=RequestContext(request))
       
    template = '%s.html' % template
    
    return render_to_response(template,
                  dict(),
                  context_instance=RequestContext(request))
    
def signup(request):
    form = forms.SignupForm(request.POST)
    if form.is_valid():
        form.save()
        user = authenticate(username=request.POST.get('username'),password=request.POST.get('password1'))
        django_login(request, user)
        return HttpResponse(simplejson.dumps([dict(status = 200)]), content_type = 'application/javascript; charset=utf8')
    else:
        return HttpResponse(simplejson.dumps([dict(status = 500)]), content_type = 'application/javascript; charset=utf8')
    
    
def remove_job(request):
    user_ci_job = models.UserCiJob.objects.get(pk=int(request.POST.get('pk')))
    user_ci_job.entity_active = False
    user_ci_job.save()
    return HttpResponse(simplejson.dumps([dict(status = 200)]), content_type = 'application/javascript; charset=utf8')

def pull_jobs(request, *args, **kwargs):
    
    if request.user.is_authenticated():
        list = get_jobs_for_user(request.user)
        for job in list:
            jenkins = RetrieveJob(job['hostname'],job['jobname'])
            result = jenkins.lookup_job()
            
            if result == urllib2.URLError:
                #TODO: add an additional state other than down 
                job['status'] = "DOWN"
            elif result == ValueError:
                #TODO: add an additional state other than down
                job['status'] = "DOWN"
            else:
                job['status'] = result['status'] 
            
        return HttpResponse(simplejson.dumps([dict(status = 200, jobs = list)]), content_type = 'application/javascript; charset=utf8')
