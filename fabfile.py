# -*- coding: utf-8 -*-

"""Build script used to test, build and deploy django-flash in several
Python versions.

In order to test and build django-flash in these different environments,
this script demands you to have different virtualenvs, each one targeted
to a specific Python version:

    * django-flash-py2.6 - for Python 2.6
    * django-flash-py2.5 - for Python 2.5
    * django-flash-py2.4 - for Python 2.4

Also, each one of these virtualenvs must have the following packages
installed:
    
    * Django (version 1.0+)
    * Pysqlite (version recommended by the current Django version)

Finally, to use this script, you must install the packages below to your
default Python installation:

    * Fabric 0.1.1+

That's it. You can now see all available targets provided by this build
script by running the command line below:

    $ cd /path/to/django-flash
    $ fab
"""

# Environment info
config.project        = 'django-flash'
config.virtualenv_dir = '~/.virtualenvs'

# Information needed to build the documentation
config.sphinx_output = 'build/sphinx'
config.sphinx_latex  = '%s/latex' % config.sphinx_output
config.sphinx_html   = '%s/html' % config.sphinx_output
config.doc_output    = 'djangoflash'

# Host where the documentation website lives
config.fab_hosts  = ['destaquenet.com']
config.doc_folder = '/home/destaquenet/public_html'

# Supported Python versions
config.versions = ('2.4', '2.5', '2.6')
config.default_version = '2.6'


def setup(command, version=config.default_version):
     """Executes the given setup command with a virtual Python installation.
     """
     local('%s/%s-py%s/bin/python setup.py %s' % (config.virtualenv_dir, config.project, version, command))

def test():
    """Runs all tests in different Python versions.
    """
    for version in config.versions:
        setup('test', version)

def clean():
    """Removes the build directory.
    """
    local('rm -fR build')

@depends(clean)
def build_docs():
    """Builds the documentation in PDF and HTML.
    """
    setup('build_sphinx')
    setup('build_sphinx -b latex')
    local('make -C ' + config.sphinx_latex)

@depends(build_docs)
def zip_docs():
    """Creates a zip file with the complete documentation.
    """
    local('cp %s/%s.pdf %s' % (config.sphinx_latex, config.project, config.sphinx_html))
    local('cd %s; mv html %s; zip -r9 %s.zip %s' % ((config.sphinx_output,) + (config.doc_output,)*3))

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
    for version in config.versions:
        setup('bdist_egg upload', version)

@depends(test, register_pypi, deploy_src, deploy_eggs)
def deploy_pypi():
    """Deploys all artifacts to PyPI.
    """
    pass

@depends(zip_docs)
def deploy_website():
    """Deploys the documentation website.
    """
    put('%s/%s.zip' % (config.sphinx_output, config.doc_output), config.doc_folder)
    run('cd %s; rm -R %s; unzip %s.zip; rm %s.zip' % ((config.doc_folder,) + (config.doc_output,)*3))

@depends(deploy_pypi, deploy_website)
def deploy():
    """Deploys the application to PyPI and updates the documentation website.
    """
    pass
