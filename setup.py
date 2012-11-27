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
			name                    = "bvd",
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