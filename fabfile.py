import subprocess, os

from fabric import api

"""Globals"""

app_name = 'ci_monitor'
wrapper = '. /usr/local/bin/virtualenvwrapper.sh;'

def install_requirements(*args,**kwargs):
	#TODO: If need be, we can add a local pypi mirror for any additional packages
	#install = 'pip install -r requirements.txt --extra-index-url %s' % (pypi_mirror)
	
	install = 'pip install -r requirements.txt'
	
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
		
def local(*args,**kwargs):
	install_requirements()