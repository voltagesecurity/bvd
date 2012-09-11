from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', include('ci_monitor.pull.urls')),
	#url(r'^listener/$', include('ci_monitor.listener.urls')),
	url(r'^js_tests$', direct_to_template, {'template': 'tests.html'}),
	url(r'^pull/', include('ci_monitor.pull.urls')),
    url(r'^openid/', include('django_openid_auth.urls')),
    url(r'^accounts/profile','ci_monitor.pull.views.redirect_to_home'),
    url(r'^admin/', include(admin.site.urls)),
	
    # url(r'^ci_monitor/', include('ci_monitor.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
