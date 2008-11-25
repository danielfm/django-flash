#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'django-flash',
    version = '1.2',
    author = 'Daniel Fernandes Martins',
    author_email = 'daniel.tritone@gmail.com',
    description = 'Rails-like flash scope support for Django.',
    license = 'LGPL',
    platforms = ['Any'],
    keywords = ['django', 'flash', 'session', 'scope', 'contrib'],
    url = 'http://github.com/danielfm/django-flash/tree/master',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP'
    ],
    install_requires = ['Django>=1.0_final'],
    packages = find_packages('src'),
    package_dir = {'':'src'},
    test_suite = 'djangoflash.tests.test_suite',
)

