from __future__ import with_statement
from setuptools import setup, find_packages
from distutils.core import setup
import os

def get_requirements(filename='requirements.txt'):
	with open(os.path.join(os.path.dirname(__file__), filename), 'rU') as f:
		return f.read().split('\n')
		
def autosetup():
	from setuptools import setup, find_packages
	return setup(
			name                    = "ci-monitor",
			version                 = "1.0",
			include_package_data    = True,
			zip_safe                = False,
			packages                = find_packages('src'),
			package_dir             = {
				''                      : 'src',
				},
			entry_points    = {
				'setuptools.file_finders' : 'git=setuptools_git:gitlsfiles'
				},
			install_requires = get_requirements()
		)

if __name__ == '__main__':
	#run setup
	autosetup()