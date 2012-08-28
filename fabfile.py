import subprocess, os, types, shlex
from multiprocessing import Process

from fabric import api

"""Globals"""

app_name = 'ci_monitor'
wrapper = '. /usr/local/bin/virtualenvwrapper.sh;'

def install_requirements(*args,**kwargs):
	#TODO: If need be, we can add a local pypi mirror for any additional packages
	#install = 'pip install -r requirements.txt --extra-index-url %s' % (pypi_mirror)
	
	install = 'pip install --user -r requirements.txt'
	
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
	cmd = shlex.split('python ./src/ci_monitor/manage.py runserver 0.0.0.0:8000')
	
	subprocess.Popen(cmd)
	
	print 'CI Monitor is running under http://localhost:8000'
	
def local(*args,**kwargs):
	"""
		Main function to be run for local development.  Function installs requirements, then starts the django dev server.
		
		Before running this function, check to make sure the CI_INSTALLATIONS tuple in settings.py is properly set to your CI servers
	"""
	install_requirements()
	start_django_dev_server()
	
def ci_build(*args,**kwargs):
	"""
		Function to be run by a CI build system.  Function installs requirements, and application to $USER's home directory.
	"""
	install_requirements()
	#TODO: Add Apache config and restart
	