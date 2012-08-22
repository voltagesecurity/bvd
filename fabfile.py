import subprocess, os

from fabric import api

"""Globals"""

app_name = 'ci_monitor'

def _do_virtualenvwrapper_command(cmd):
	""" This is tricky, because all virtualenwrapper commands are
		actually bash functions, so we can't call them like we would other executables.
	"""

	out, err = subprocess.Popen(
		['bash', '-c', '. /usr/local/bin/virtualenvwrapper.sh; %s' % cmd],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	print(out)
	print(err)

def install_requirements(*args,**kwargs):
	#TODO: If need be, we can add a local pypi mirror for any additional packages
	#install = 'pip install -r requirements.txt --extra-index-url %s' % (pypi_mirror)
	
	install = 'pip install -r requirements.txt'
	
	if kwargs.get('remote'):
		api.run('%(install)s' % dict(install=install))
	else:
		#create virtual env
		_do_virtualenvwrapper_command('mkvirtualenv %s' % app_name)
		_do_virtualenvwrapper_command('workon %s' % app_name)
		
		#install requirements
		install = '%s -e %s' % (install, os.getcwd())
		api.local('%(install)s' % dict(
				install = install
			))
			
def local(*args,**kwargs):
	install_requirements()