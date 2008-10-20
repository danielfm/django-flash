# -*- coding: utf-8 -*-

"""
Test cases used to check the behavior of django-flash classes.
"""

from django.http import HttpRequest, HttpResponse
from django.test import TestCase

import django_flash.context_processors as context_processors
from django_flash.middleware import FlashMiddleware


class FlashContextProcessorTestCase(TestCase):
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


class FlashMiddlewareTestCase(TestCase):
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
