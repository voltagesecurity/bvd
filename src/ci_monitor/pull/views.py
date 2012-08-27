from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse

def home(request,template='index.html'):
	return render_to_response(template,
	                          dict(title='Welcome to CI-Monitor'),
	                          context_instance=RequestContext(request))
	
def poll_jenkins_servers(request):
	if request.is_ajax():
		"""
		result = []
		for i in range(0,30):
			d = dict(
					job_name = 'Job%d' % i,
					status   = 'success' if i % 2 == 0 else 'failed',
				)
			result.append(d)
		"""
		
		return HttpResponse(simplejson.dumps(result), mimetype='application/javascript')
	else:
		raise RuntimeError('Improper use of View')
		
	