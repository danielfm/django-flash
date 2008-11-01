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
        "Flash message should not be accessible when not previously defined."
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
    
    def _process_request(self, func=None):
        "Simulates a subset of the request/response cycle."
        self.middleware.process_request(self.request)
        if func and callable(func):
            func()
        self.middleware.process_response(self.request, self.response)
    
    def test_presence_of_flash_scope(self):
        "FlashScope object should be made available in the request object."
        self._process_request()
        self.assertTrue(hasattr(self.request, 'flash'))
    
    def test_without_flash_message(self):
        "Flash message should not be accessible when not previously defined."
        self._process_request()
        self.assertFalse(self.request.session.has_key('flash'))
    
    def test_none_flash_message(self):
        "Flash message set to None should not be available at the session."
        def empty_message():
            self.request.flash = None
        self._process_request(empty_message)
        self.assertFalse(self.request.session.has_key('flash'))
    
    def test_empty_flash_message(self):
        "Flash message set to '' should not be available at the session."
        def empty_message():
            self.request.flash = ''
        self._process_request(empty_message)
        self.assertFalse(self.request.session.has_key('flash'))
    
    def test_with_flash_message(self):
        "Flash message should be accessible when previously defined."
        def string_flash_message():
            self.request.flash = 'Hey'
        self._process_request(string_flash_message)
        self.assertEquals('Hey', self.request.session['flash'])
    
    def test_flash_with_map_syntax(self):
        "Flash attribute should support map syntax, like flash['property']."
        def map_syntax_flash_message():
            self.request.flash['something'] = 'Yikes'
        self._process_request(map_syntax_flash_message)
        self.assertEquals('Yikes', self.request.session['flash']['something'])
    
    def test_flash_with_member_syntax(self):
        "Flash attribute should support member syntax, like flash.property."
        def attribute_syntax_flash_message():
            self.request.flash.something = 'Outch'
        self._process_request(attribute_syntax_flash_message)
        self.assertEquals('Outch', self.request.session['flash'].something)
    
    def test_flash_with_map_object(self):
        "Flash message set to a map object should work as expected."
        def map_flash_message():
            self.request.flash = {'abc': 'def'}
        self._process_request(map_flash_message)
        self.assertEquals('def', self.request.session['flash']['abc'])
    
    def test_flash_with_empty_map_object(self):
        "Flash message set to an empty map object should work as expected."
        def empty_map_flash_message():
            self.request.flash = {}
        self._process_request(empty_map_flash_message)
        self.assertFalse(self.request.session.has_key('flash'))
    
    def test_flash_with_array_object(self):
        "Flash message set to an array object should work as expected."
        def array_flash_message():
            self.request.flash = ['abc']
        self._process_request(array_flash_message)
        self.assertEqual('abc', self.request.session['flash'][0])
    
    def test_flash_with_empty_array_object(self):
        "Flash message set to an empty array object should work as expected."
        def empty_array_flash_message():
            self.request.flash = []
        self._process_request(empty_array_flash_message)
        self.assertFalse(self.request.session.has_key('flash'))
