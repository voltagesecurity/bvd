from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('ci_monitor.pull.views',
    
    url(r'^$', 'home',name='home'),
    url(r'^pull_jobs/$','pull_jobs',name='pull_jobs'),
	url(r'^validate_hostname/$','validate_hostname',name='validate_hostname'),
    url(r'^validate_username/$','validate_username',name='validate_username'),
	url(r'^validate_job/$','validate_job',name='validate_job'),
	url(r'^retrieve_job/$','retrieve_job',name='retrieve_job'),
    url(r'^signup/$','signup',name='signup'),
    url(r'^remove_job/$','remove_job',name='remove_job'),
	url(r'^autocomplete_hostname/$','autocomplete_hostname',name='autocomplete_hostname'),
	#url(r'^save_job/$','save_job',name='save_job'),
    url(r'^save_jobs/$','save_jobs',name='save_jobs'),
	url(r'^get_modal/$','get_modal',name='get_modal'),
    url(r'^login/$','login',name='login'),
    url(r'^logout/$','logout',name='logout'),
	
)
