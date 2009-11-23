# -*- coding: utf-8 -*-

"""Build script used to test, build and deploy django-flash using several
Python versions.

In order to test and build django-flash in these different environments,
this script requires different virtualenvs, each one targeted to a specific
Python version:

    * django-flash-py2.6 - for Python 2.6
    * django-flash-py2.5 - for Python 2.5
    * django-flash-py2.4 - for Python 2.4

Also, each one of these virtualenvs must have the following packages
installed:
    
    * Django   (version 1.0+)
    * Pysqlite (version recommended by the current Django version)

Finally, to use this script, you must install the packages below to your
default Python installation:

    * Fabric 0.9+

That's it. You can now see all available targets provided by this build
script by running the command line below:

    $ cd /path/to/django-flash
    $ fab -l
"""

import os
import re
import sys

from fabric.api import *


# Adds the 'src' to the Python path
sys.path += ('src',)

# Supported Python versions
env.versions        = ('2.6', '2.5', '2.4')
env.default_version = env.versions[0]

# Environment info
env.project        = 'django-flash'
env.virtualenv_dir = os.environ['WORKON_HOME'] or '~/.virtualenvs'
env.default_editor = os.environ['EDITOR']      or 'vi'

# Files that contain version information
env.new_version_files = (
    'setup.py',
    'src/djangoflash/__init__.py',
    'doc/source/conf.py',
    'doc/source/changelog.rst',
)

# Information needed to build the documentation
env.sphinx_output = 'build/sphinx'
env.sphinx_latex  = '%s/latex' % env.sphinx_output
env.sphinx_html   = '%s/html' % env.sphinx_output
env.doc_output    = 'djangoflash'

# Host where the documentation website lives
env.hosts  = ['destaquenet.com']
env.doc_folder = '/home/destaquenet/public_html'


def setup(command, version=env.default_version):
     """Executes the given setup command with a virtual Python installation.
     """
     local('%s/%s-py%s/bin/python setup.py %s' %
             (env.virtualenv_dir, env.project, version, command))

def test():
    """Runs all tests in different Python versions.
    """
    for version in env.versions:
        setup('test', version)

def clean():
    """Removes the build directory.
    """
    local('rm -fR build')

def build_docs():
    """Builds the documentation in PDF and HTML.
    """
    clean()
    setup('build_sphinx')
    setup('build_sphinx -b latex')
    local('make -C ' + env.sphinx_latex)

def zip_docs():
    """Creates a zip file with the complete documentation.
    """
    build_docs()
    local('cp %s/%s.pdf %s' %
            (env.sphinx_latex, env.project, env.sphinx_html))
    local('cd %s; mv html %s; zip -r9 %s.zip %s' %
            ((env.sphinx_output,) + (env.doc_output,)*3))

def register_pypi():
    """Register the current version on PyPI.
    """
    setup('register')

def deploy_src():
    """Deploy the source code to PyPI.
    """
    setup('sdist upload')

def deploy_eggs():
    """Upload Python Eggs to PyPI.
    """
    for version in env.versions:
        setup('bdist_egg upload', version)

def deploy_pypi():
    """Deploys all artifacts to PyPI.
    """
    test()
    register_pypi()
    deploy_src()
    deploy_eggs()

def deploy_website():
    """Deploys the documentation website.
    """
    zip_docs()
    put('%s/%s.zip' %
            (env.sphinx_output, env.doc_output), env.doc_folder)
    run('cd %s; rm -R %s; unzip %s.zip; rm %s.zip' %
            ((env.doc_folder,) + (env.doc_output,)*3))

def deploy():
    """Deploys the application to PyPI and updates the documentation website.
    """
    deploy_pypi()
    deploy_website()

def tag_new_version():
    """Updates the version number, pushing the changes and tagging afterwards.
    """
    # Checks if there are changed or untracked files
    git_status_file = 'build/git_status'
    local('git status > %s' % git_status_file, fail='ignore')
    if re.search(r'(Changed|Untracked)', file(git_status_file, 'r').read()):
        print 'There are changed or untracked files. Aborting...'
        return

    # Brings up the text editor with the files to be changed
    for f in env.new_version_files:
        local('%s %s' % (env.default_editor, f))

    # Asks for confirmation
    prompt('tag_proceed', 'You are about to commit and push the version '
                          'changes. Continue?', default='y')

    if env.tag_proceed.upper() != 'Y':
        print 'Aborting...'
        return

    # Commits and tags the new release
    from djangoflash import __version__
    local('git commit -am "Updated version number."; git push', fail='ignore')
    local('git tag -am "Tagged version %s." %s; git push --tags' %
            ((__version__,)*2), fail='ignore')
    local('git push --tags')

