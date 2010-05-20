#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name = 'django-flash',
    version = '1.7.2',
    author = 'Daniel Fernandes Martins',
    author_email = 'daniel@destaquenet.com',
    description = 'Django-flash is a simple Django extension which provides support for Rails-like flash messages.',
    license = 'BSD',
    platforms = ['Any'],
    keywords = ['django', 'flash', 'session', 'scope', 'context', 'contrib'],
    url = 'http://djangoflash.destaquenet.com/',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP'
    ],
    install_requires = ['Django>=1.0_final'],
    packages = find_packages('src'),
    package_dir = {'':'src'},
    include_package_data = True,
    zip_safe = False,
    test_suite = 'djangoflash.tests.suite',
)

