from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('ci_monitor.pull.views',
    
    url(r'^$', 'home',name='home'),
	url(r'^get_jenkins_views/$','poll_jenkins_servers',name='poll_jenkins_view'),
	url(r'^validate_hostname/$','validate_hostname',name='validate_hostname'),
	url(r'^retrieve_job/$','retrieve_job',name='retrieve_job'),
	url(r'^start_j2/$','start_jenkins2'),
	url(r'^stop_j2/$','stop_jenkins2'),
	url(r'^start_j3/$','start_jenkins3'),
	url(r'^stop_j3/$','stop_jenkins3'),
	
)
