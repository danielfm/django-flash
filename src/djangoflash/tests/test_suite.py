# -*- coding: utf-8 -*-

"""
Test cases used to check the behavior of django-flash classes.
"""

import unittest

from django.http import HttpRequest, HttpResponse

import djangoflash.context_processors as context_processors
from djangoflash.middleware import FlashMiddleware


# Pointing to an empty module to make Django objects "think"
# they are inside a regular Django project

import os
os.environ['DJANGO_SETTINGS_MODULE'] = \
    'djangoflash.tests.django_project_settings'


class FlashContextProcessorTestCase(unittest.TestCase):
    """
    FlashContextProcessor test case.
    """
    
    def setUp(self):
        "Create a request with an empty session."
        self.request = HttpRequest()
        self.request.session = {}
    
    def test_without_flash_message(self):
        "Flash message shouldn't be accessible when not previously defined."
        context = context_processors.flash(self.request)
        self.assertFalse(context['flash'])
    
    def test_with_flash_message(self):
        "Flash message should be accessible when previously defined."
        self.request.session['flash'] = 'Something'
        self.assertTrue(self.request.session.has_key('flash'))
        
        context = context_processors.flash(self.request)
        self.assertFalse(self.request.session.has_key('flash'))
        self.assertTrue(context.has_key('flash'))
        self.assertEqual('Something', context['flash'])


class FlashMiddlewareTestCase(unittest.TestCase):
    """
    FlashMiddleware test case.
    """
    
    def setUp(self):
        "Configure the request and response objects."
        self.request = HttpRequest()
        self.request.session = {}
        self.response = HttpResponse()
        self.middleware = FlashMiddleware()
    
    def test_without_flash_message(self):
        "Flash message should not be accessible when not previously defined."
        self.middleware.process_response(self.request, self.response)
        self.assertFalse(self.request.session.has_key('flash'))
    
    def test_with_flash_message(self):
        "Flash message should be accessible when previously defined."
        self.request.flash = 'Something'
        self.middleware.process_response(self.request, self.response)
        self.assertTrue(self.request.session.has_key('flash'))
