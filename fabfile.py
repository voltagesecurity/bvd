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
import subprocess, os, types, shlex, re
from multiprocessing import Process

from fabric import api

"""Globals"""

app_name = 'bvd'
wrapper = '. /usr/local/bin/virtualenvwrapper.sh;'
path_to_bvd = '/opt/bvd'

def install_requirements(*args,**kwargs):
    #TODO: If need be, we can add a local pypi mirror for any additional packages
    #install = 'pip install -r requirements.txt --extra-index-url %s' % (pypi_mirror)
    
    install = 'pip install --upgrade --user -r requirements.txt'
    
    if kwargs.get('remote'):
        api.run('%(install)s' % dict(install=install))
    else:
        #check if user
        
        
        #TODO: provide arguments: whether a user wants to use a virtualenv
        #mkvirtualenv = '%s %s' % (wrapper,'mkvirtualenv %s' % app_name)
        #workon = '%s %s' % (wrapper,'workon %s' % app_name)
        
        install = '%s -e %s' % (install, os.getcwd())
        
        #cmd = '%s ; %s ; %s' % (mkvirtualenv, workon, install)
        cmd = install
        
        out, err = subprocess.Popen(cmd,shell=True).communicate()
        
def start_django_dev_server(*args,**kwargs):
    cmd = 'cd ./src/bvd && python manage.py runserver 0.0.0.0:8000'
    
    subprocess.call(cmd, shell=True)
    
    print 'CI Monitor is running under http://localhost:8000'

def sync_db(*args,**kwargs):
    cmd = 'cd ./src/bvd && python manage.py syncdb --noinput'
    subprocess.call(cmd,shell=True)

def migrate_db(*args, **kwargs):
    cmd = 'cd ./src/bvd && python manage.py migrate'
    subprocess.call(cmd, shell=True)

def git_pull(*args, **kwargs):
    """
    This function:
        Updates the local repository by runnning `git pull`
    """
    subprocess.call('git pull', shell=True)
    
def local(*args,**kwargs):
    """
        Main function to be run for local development.  Function installs requirements, then starts the django dev server.
        
        Before running this function, check to make sure the CI_INSTALLATIONS tuple in settings.py is properly set to your CI servers
    """
    install_requirements()
    sync_db()
    start_django_dev_server()
    
def ci_build(*args,**kwargs):
    """
        Function to be run by a CI build system.  Function installs requirements, and application to $USER's home directory.
    """
    install_requirements()
    #TODO: Add Apache config and restart
    
def configure_apache(*args, **kwargs):
    """
    This function:
        1 - Tells the user to add these two lines to /etc/apache2/httpd.conf:
               LoadModule wsgi_module libexec/apache2/mod_wsgi.so
               Include {{ path_to_bvd}}/src/config/bvd.conf
            where {{ path_to_bvd }} is the location of the installation of BVD
        2 - In src/config/bvd.conf.template, replaces {{ path_to_bvd }} with the location of the installation of BVD
        3 - Moves to src/config/bvd.conf
        4 - Tells the user to restart apache with `apachectl -k restart`
    """
    
    print "Add these two lines to the appropriate places in /etc/apache2/httpd.conf:"
    print "LoadModule wsgi_module libexec/apache2/mod_wsgi.so"
    print "Include {{ path_to_bvd }}/src/config/bvd.conf"
    print "where {{ path_to_bvd }} is the location of the installation of BVD"

    # Check for the existence of bvd.conf before the template is 'rendered'
    bvd_config_exists = os.path.isfile("%s/src/config/bvd.conf" % path_to_bvd)

    # Render the template to the correct location
    if not bvd_config_exists:
        with open("%s/src/config/bvd.conf.template" % path_to_bvd, 'r') as template:
            with open("%s/src/config/bvd.conf" % path_to_bvd, 'w') as destination:
                for line in template:
                    destination.write(re.sub(r"{{ *path_to_bvd *}}", path_to_bvd, line))
    
    # Restart Apache
    print "Then restart apache with `apachectl -k restart`"
    


def configure_automatic_start_on_login_osx(*args, **kwargs):
    """
    This Function:
        1 - Checks for/creates directory ~/Library/LaunchAgents
        2 - copies src/config/com.user.loginscript.plist.template to ~/Library/LaunchAgents/
        3 - replaces {{ path_to_bvd }} with the location of the installation of BVD
        4 - moves com.user.loginscript.plist.template to com.user.loginscript.plist
        5 - calls `launchctl load ~/Library/LaunchAgents/com.user.loginscript.plist`
        6 - outputs a message to STDOUT asking the user to test that the script works by calling
            `launchctl start com.user.loginscript`
    """
    os.path.exists(os.path.expanduser("~/Library/LaunchAgents"))
    with open("%s/src/config/com.user.loginscript.plist.template" % path_to_bvd, 'r') as template:
        with open(os.path.expanduser("~/Library/LaunchAgents/com.user.loginscript.plist"), 'w') as destination:
            for line in template:
                destination.write(re.sub(r"{{ *path_to_bvd *}}", path_to_bvd, line))
    subprocess.call(["launchctl", "load", os.path.expanduser("~/Library/LaunchAgents/com.user.loginscript.plist")])
    print "test that the automatic launch script works by calling `launchctl start com.user.loginscript`"


def update_bvd(*args, **kwargs):
    """
    This function:
        1 - Updates the local repository
        2 - Syncs the database
    """
    git_pull()
    sync_db()
