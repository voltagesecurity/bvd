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
	
def kill_django_dev_server(*args,**kwargs):
	cmd1 = 'ps aux | grep \"manage.py runserver\"'
	cmd2 = 'awk {\'print $2\'}'
	
	proc1 = subprocess.Popen(cmd1,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)	
	proc2 = subprocess.Popen(['-c', cmd2],stdin=proc1.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
	
	pids = [id for id in proc2.communicate()[0].split('\n')  if id.isdigit()]
	
	for pid in pids:
		subprocess.call(shlex.split('kill -9 %s' % pid))
		
def start_django_dev_server(*args,**kwargs):
	cmd = shlex.split('./src/ci_monitor/manage.py runserver 0.0.0.0:8000')
	
	subprocess.Popen(cmd)
	
	print 'CI Monitor is running under http://localhost:8000'
	
def local(*args,**kwargs):
	install_requirements()
	#kill_django_dev_server()
	start_django_dev_server()
	