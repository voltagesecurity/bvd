import urllib2, types

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.conf import settings

from ci_monitor.jenkins.jenkins import PollCI

def home(request,template='index.html'):
    return render_to_response(template,
                              dict(title='Welcome to CI-Monitor'),
                              context_instance=RequestContext(request))
                              
def poll_jenkins(jenkins, host, json_list):
    _dict,ns = jenkins.read_rss()
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
        json1 = jenkins.poll(entry,ns)
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
            
        if 'hosts' in request.POST:
            l = simplejson.loads(request.POST['hosts'])
            hosts = []
            for d in l:
                for k,v in d.iteritems():
                    hosts.append(dict(hostname=k,json=v))
        else:
            hosts = settings.CI_INSTALLATIONS
        
        results = poll_ci(hosts)
        print '>>>>>>>>>>>>>>>>> results %s' % results
        return HttpResponse(simplejson.dumps(results), content_type = 'application/javascript; charset=utf8')
        #if results == []:
        #   raise RuntimeError('Please check jenkins URIs in settings.py')
    else:
        raise RuntimeError('Improper use of View')
        
def start_jenkins(request):
	import subprocess
	import shlex
	suprocess.Popen(shlex.split('/srv/tomcat2/bin/startup.sh'),shell=True).communicate()
        return HttpResponse(simplejson.dumps(['started']))

def stop_jenkins(request):
	import subprocess
	import shlex
	subprocess.Popen(shlex.split('/srv/tomcat2/bin/shutdown.sh'),shell=True).communicate()
	return HttpResponse(simplejson.dumps(['stopped']))
