"""
BVD v1.0

Copyright (c) 2012 Voltage Security
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. The name of the author may not be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.conf import settings

urlpatterns = patterns('bvd.pull.views',
    
  url(r'^$', 'home',name='home'),
  url(r'^pull_jobs/$','pull_jobs',name='pull_jobs'),
  url(r'^pull_apple_tv_jobs/$', 'pull_apple_tv_jobs', name='pull_apple_tv_jobs'),
  url(r'^pull_all_display_jobs/$', 'pull_all_display_jobs', name='pull_all_display_jobs'),
  url(r'^pull_jobs_for_product/$', 'pull_jobs_for_product', name='pull_jobs_for_product'),
  url(r'^validate_hostname/$','validate_hostname',name='validate_hostname'),
  url(r'^validate_username/$','validate_username',name='validate_username'),
  url(r'^validate_job/$','validate_job',name='validate_job'),
  url(r'^add_job/$', 'add_job', name='add_job'),
  url(r'^remove_job/$','remove_job',name='remove_job'),
  url(r'^autocomplete_hostname/$','autocomplete_hostname',name='autocomplete_hostname'),
  url(r'^save_jobs/$','save_jobs',name='save_jobs'),
  url(r'^get_modal/$','get_modal',name='get_modal'),
  url(r'^login/$','login',name='login'),
  url(r'^logout/$','logout',name='logout'),
  url(r'^save_widget/$', 'save_widget', name='save_widget'),
  url(r'^add_product/$', 'add_product', name='add_product'),
  url(r'^save_product/$', 'save_product', name='save_product'),
  url(r'^remove_product/$', 'remove_product', name='remove_product'),
  url(r'^edit_widget_image/$','edit_widget_image',name='edit_widget_image'),
  url(r'^product/(?P<productname>\w*)/$', 'view_product', name='view_product'),
)
