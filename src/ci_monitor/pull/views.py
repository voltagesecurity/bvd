import urllib2, types

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login

import memcache
memc = memcache.Client(['127.0.0.1:11211'], debug=1)

from ci_monitor.jenkins.jenkins import PollCI, RetrieveJob
from ci_monitor.pull import models
from ci_monitor.pull import forms

def append_http(hostname):
    if not hostname: return 'http://'
    
    if hostname.find('http') > -1 or hostname.find('https') > -1:
        return hostname
    else:
        return 'http://%s' % hostname

def home(request,template='index.html'):
    jobs = models.CiJob.objects.filter(entity_active=True)
    return render_to_response(template,
                              dict(title='Welcome to CI-Monitor', jobs = jobs),
                              context_instance=RequestContext(request))
            
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
        result.update(dict(hostname = request.POST.get('hostname')))
        
    key = str('%s/%s' % (hostname, jobname))
    
    memc.set(key,result)

    return HttpResponse(simplejson.dumps([dict(status = 200)]), content_type = 'application/javascript; charset=utf8')
    
def retrieve_job(request):
    hostname = append_http(request.POST.get('hostname',''))
    jobname = request.POST.get('jobname',None)
    displayname = request.POST.get('displayname')
    
    if hostname.strip() == 'http://' or not jobname:
        result = [dict(status = 500)]
        return HttpResponse(simplejson.dumps(result), content_type = 'application/javascript; charset=utf8')
        
    #check to see if job already exists in DB with entity active
    try:
        job = models.CiJob.objects.get(jobname=jobname,ci_server__hostname=hostname,entity_active=True)
        exists = True
    except ObjectDoesNotExist:
        exists = False
    
    if exists:
        result = dict(status = 100)
        return HttpResponse(simplejson.dumps([result]), content_type = 'application/javascript; charset=utf8')
    
    key = str('%s/%s' % (hostname, jobname))
    result = memc.get(key)
    
    if not result:
        print 'NO MEMCACHED'
        result = dict(status = 500)
        return HttpResponse(simplejson.dumps([result]), content_type = 'application/javascript; charset=utf8')
        
    result.update(dict(displayname = displayname, jobname = displayname))
        
    return HttpResponse(simplejson.dumps([result]), content_type = 'application/javascript; charset=utf8')
    
def save_job(**widget):
    hostname = append_http(widget.get('hostname',''))
    jobname = widget.get('jobname')
    left = widget.get('left')
    top = widget.get('top')
    status = widget.get('status')
    displayname = widget.get('displayname')
    width = widget.get('width')
    height = widget.get('height')

    if hostname.strip() == '' or not bool(jobname) or not bool(left) or not bool(top):
        result = [dict(status = 500)]
        #return result
        
    try:
        server = models.CiServer.objects.get(hostname=hostname)
    except ObjectDoesNotExist:
        server = models.CiServer(hostname=hostname)
        server.save()
        
    try:
        job = models.CiJob.objects.get(jobname=jobname,ci_server__hostname=hostname,entity_active=True)
        job.left_position = left
        job.top_position = top
        job.width = width
        job.height = height
        job.status = status
        job.save()
    except ObjectDoesNotExist:
        job = models.CiJob(jobname=jobname, left_position=left, top_position=top, entity_active=True, status=status, displayname=displayname, width=width, height=height)
        job.ci_server = server
        job.save()
        
    result = dict(status = 200)
    #return result

def save_jobs(request):
    widgets = simplejson.loads(request.POST['widgets'])
    for widget in widgets:
        save_job(**widget)
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
    template = '%s.html' % template
    
    return render_to_response(template,
                  dict(title='Welcome to CI-Monitor'),
                  context_instance=RequestContext(request))
    
def signup(request):
    form = forms.SignupForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(user)
        return HttpResponse(simplejson.dumps([dict(status = 200)]), content_type = 'application/javascript; charset=utf8')
    else:
        return HttpResponse(simplejson.dumps([dict(status = 500)]), content_type = 'application/javascript; charset=utf8')
    
def poll_jenkins_servers(request, *args, **kwargs):
    
    results = []
    widgets = simplejson.loads(request.POST['widgets'])
    for widget in widgets:
        job = RetrieveJob(widget.get('hostname'),widget.get('jobname'))
        result = job.lookup_job()
        if result == urllib2.URLError:
            result = dict(status = 500)
        elif result == ValueError:
            result = dict(status = 404)
        else:
            result.update({'hostname' : widget.get('hostname')})
            results.append(result)
    
    return HttpResponse(simplejson.dumps(results), content_type = 'application/javascript; charset=utf8')
