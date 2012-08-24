from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request,template='index.html'):
	return render_to_response(template,
	                          dict(title='Welcome to CI-Monitor'),
	                          context_instance=RequestContext(request))
	