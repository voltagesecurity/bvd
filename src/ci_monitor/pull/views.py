import urllib2, types

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import memcache
memc = memcache.Client(['127.0.0.1:11211'], debug=1)

from ci_monitor.jenkins.jenkins import PollCI, RetrieveJob
from ci_monitor.pull import models

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
    if not bool(displayname): displayname = jobname
    
    if hostname.strip() == 'http://' or not jobname:
        result = [dict(status = 500)]
        return HttpResponse(simplejson.dumps(result), content_type = 'application/javascript; charset=utf8')
    
    key = str('%s/%s' % (hostname, jobname))
    result = memc.get(key)
    
    if not result:
        result = dict(status = 500)
        return HttpResponse(simplejson.dumps([result]), content_type = 'application/javascript; charset=utf8')
        
    result.update(dict(displayname = displayname))
        
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
        job.left_positon = left
        job.top_position = top
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
    result = dict(status = 200)
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
        template = 'add_job.html'
    
    return render_to_response(template,
                  dict(title='Welcome to CI-Monitor'),
                  context_instance=RequestContext(request))
                              
def poll_jenkins(jenkins, host, json_list):
    _dict,ns = jenkins.read_rss()
    print 'IN POLL JENKINS' 
    print _dict,ns
    if _dict is None:
        if ns == urllib2.URLError:
            for elem in json_list:
                elem['status'] = 'DOWN'
            return None,None
        if ns == urllib2.HTTPError:
            for elem in json_list:
                elem['status'] = '404'
            return None,None
    return _dict['elements'], ns
    
def process_entries(jenkins, entries, _dictionary, host, toRTN, ns):
    to_return = []
    _d = dict(
        hostname = host if not _dictionary else host.get('hostname'),
        json = to_return,
    )
    for entry in entries:
        print 'entry is %s' % entry 
        json1 = jenkins.poll(entry,ns)
        print 'json is %s' % json1
        if json1 is None:
            continue
        to_return.append(json1)
    
    if _dictionary:
        host['json'] = to_return
    else:
        toRTN.append(_d)
                              
def poll_ci(hosts):
    toRTN = []
    
    for host in hosts:
        if type(host) == types.DictType:
            hostname = host.get('hostname')
            _dictionary = True
        else:
            hostname = host
            _dictionary = False

        jenkins = PollCI(hostname)
        
        if _dictionary: json_list = host.get('json')
        else: json_list = []
        
        entries, ns = poll_jenkins(jenkins, host, json_list)
        print '>>>>>>>>>>>>>>json_list %s ' % json_list
        if entries is None:
            continue
            
        process_entries(jenkins, entries, _dictionary, host, toRTN, ns)

    if _dictionary:
        return hosts
    else:
        return toRTN
    
    
def poll_jenkins_servers(request, *args, **kwargs):
    if request.is_ajax():
        print request.POST
        """
        if 'hosts' in request.POST:
            l = simplejson.loads(request.POST['hosts'])
            hosts = []
            for d in l:
                for k,v in d.iteritems():
                    hosts.append(dict(hostname=k,json=v))
        else:
            hosts = settings.CI_INSTALLATIONS
        
        results = poll_ci(hosts)
        """    
        results = []
        for i in range(5):
            results.append(dict(hostname='http://localhost:80%d' % i, json = [dict(job_name = 'Server-%d-Job-%d' % (i,x),status='SUCCESS' if x%2 ==0 else 'FAILURE') for x in range(0,5)]))
        print '>>>>>>>>>>>>>>>>> results %s' % results
        return HttpResponse(simplejson.dumps(results), content_type = 'application/javascript; charset=utf8')
        #if results == []:
        #   raise RuntimeError('Please check jenkins URIs in settings.py')
    else:
        raise RuntimeError('Improper use of View')
        
def start_jenkins2(request):
    import subprocess
    import shlex
    subprocess.Popen(shlex.split('/srv/tomcat2/bin/startup.sh'),shell=True).communicate()
    return HttpResponse(simplejson.dumps(['started']))

def stop_jenkins2(request):
    import subprocess
    import shlex
    subprocess.Popen(shlex.split('/srv/tomcat2/bin/shutdown.sh'),shell=True).communicate()
    return HttpResponse(simplejson.dumps(['stopped']))

def start_jenkins3(request):
    import subprocess
    import shlex
    subprocess.Popen(shlex.split('/srv/tomcat3/bin/startup.sh'),shell=True).communicate()
    return HttpResponse(simplejson.dumps(['started']))

def stop_jenkins3(request):
    import subprocess
    import shlex
    subprocess.Popen(shlex.split('/srv/tomcat3/bin/shutdown.sh'),shell=True).communicate()
    return HttpResponse(simplejson.dumps(['stopped']))
