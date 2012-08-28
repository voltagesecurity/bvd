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
	
def poll_jenkins_servers(request,*args,**kwargs):
	if request.is_ajax():
		jenkins = PollCI(settings.CI_INSTALLATIONS)
		result = jenkins.poll()
		if result == []:
			raise RuntimeError('Please check jenkins URIs in settings.py')
		return HttpResponse(simplejson.dumps(result), content_type = 'application/javascript; charset=utf8')
	else:
		raise RuntimeError('Improper use of View')
		
	