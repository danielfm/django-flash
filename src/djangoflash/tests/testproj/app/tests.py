# -*- coding: utf-8 -*-

"""Project's test cases.
"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from testproj.app import views

from djangoflash.middleware import FlashScope


class FlashScopeTestCase(TestCase):
    """Test the FlashScope object.
    """
    
    def setUp(self):
        "Create a FlashScope object to be used by the test methods."
        self.scope = FlashScope()
    
    def test_contains_inactive_object(self):
        "Inactive flash scoped objects should fail at __contains__()."
        self.scope['key'] = 'value'
        self.assertTrue('key' not in self.scope)
    
    def test_contains_active_object(self):
        "Active flash scoped objects should be visible at __contains__()."
        self.scope['key'] = 'value'
        self.scope.increment_age()
        self.assertTrue('key' in self.scope)
    
    def test_get_inactive_object(self):
        "Inactive flash scoped objects should raise KeyError at __getitem__()."
        def method():
            return self.scope['key']
        self.scope['key'] = 'value'
        self.assertRaises(KeyError, method)
    
    def test_get_active_object(self):
        "Active flash scoped objects should be retrieved at __getitem__()."
        self.scope['key'] = 'value'
        self.scope.increment_age()
        self.assertEqual('value', self.scope['key'])
    
    def test_pop_inactive_object(self):
        "Inactive flash scoped objects should raise KeyError at pop()."
        def method():
            return self.scope.pop('key')
        self.scope['key'] = 'value'
        self.assertRaises(KeyError, method)
    
    def test_pop_active_object(self):
        "Active flash scoped objects should be retrieved at pop()."
        self.scope['key'] = 'value'
        self.scope.increment_age()
        self.assertEqual('value', self.scope.pop('key'))
    
    def test_delete_object(self):
        "Flash scoped objects should be removed at del flash['key']."
        self.scope['key'] = 'value'
        self.scope.increment_age()
        del self.scope['key']
        self.assertTrue('key' not in self.scope)
    
    def test_is_current_empty(self):
        "Current flash scoped objects should be considered at is_current_empty()"
        self.scope['key'] = 'value'
        self.assertFalse(self.scope.is_current_empty())
        
        self.scope.increment_age()
        self.assertFalse(self.scope.is_current_empty())
        
        self.scope.increment_age()
        self.assertTrue(self.scope.is_current_empty())
    
    def test_is_active_empty(self):
        "Only active flash scoped objects should be considered at is_active_empty()."
        self.scope['key'] = 'value'
        self.assertTrue(self.scope.is_active_empty())
        
        self.scope.increment_age()
        self.assertFalse(self.scope.is_active_empty())
    
    def test_has_inactive_key(self):
        "Inactive flash scoped objects should return False at has_key()."
        self.scope['key'] = 'value'
        self.assertFalse(self.scope.has_key('key'))
    
    def test_has_active_key(self):
        "Active flash scoped objects should return True at has_key()."
        self.scope['key'] = 'value'
        self.scope.increment_age()
        self.assertTrue(self.scope.has_key('key'))
    
    def test_keys(self):
        "Only active flash scoped objects should be considered at keys()."
        self.scope['key'] = 'value'
        self.assertFalse(self.scope.keys())
        
        self.scope.increment_age()
        self.assertEqual(['key'], self.scope.keys())
    
    def test_values(self):
        "Only active flash scoped objects should be considered at values()."
        self.scope['key'] = 'value'
        self.assertFalse(self.scope.values())
        
        self.scope.increment_age()
        self.assertEqual(['value'], self.scope.values())
    
    def test_items(self):
        "Only active flash scoped objects should be considered at items()."
        self.scope['key'] = 'value'
        self.assertFalse(self.scope.items())
        
        self.scope.increment_age()
        self.assertEqual([('key', 'value')], self.scope.items())
    
    def test_put(self):
        "The put() method should work the same way as __setitem__()."
        self.scope.put(key='value')
        self.scope.increment_age()
        self.assertEqual('value', self.scope['key'])
    
    def test_now(self):
        "Objects added with flash.now() should be active right away."
        self.scope.now(key='value')
        self.assertEqual('value', self.scope['key'])
    
    def test_keep(self):
        "The flash.skip() method should delay objects expiration."
        def method():
            return self.scope['key']
        self.scope['key'] = 'value'
        self.scope.increment_age()
        
        for num in range(3):
            for num2 in range(3):
                self.scope.keep('key')
            self.scope.increment_age()
            self.assertEqual('value', self.scope['key'])
        
        self.scope.increment_age()
        self.assertRaises(KeyError, method)


class DjangoFlashTestCase(TestCase):
    """Test the middleware and the context processors working within a real
    Django application.
    """
    def test_invalid_flash(self):
        "Test flash context with an invalid object."
        def invalid():
            self.client.get(reverse(views.invalid_flash))
        self.assertRaises(TypeError, invalid)
    
    def test_dict_syntax(self):
        "Map syntax should be available to put objects in flash context."
        self.response = self.client.post(reverse(views.dict_syntax))
        self.response = self.client.get(reverse(views.render_template))
        self.assertEqual('Oops', self.response.context['flash']['message'])
    
    def test_now(self):
        "Try to access a 'now' flash variable in the same request."
        self.response = self.client.get(reverse(views.now))
        self.assertEqual('Nice!', self.response.context['flash']['message'])
    
    def test_now_expiration(self):
        "Try to access a 'now' flash variable in the next request."
        self.response = self.client.get(reverse(views.now))
        self.response = self.client.get(reverse(views.render_template))
        self.assertTrue(self.response.context['flash'].is_active_empty())
    
    def test_flash_early_access(self):
        "Try to access a flash variable too soon."
        self.response = self.client.get(reverse(views.flash_early_access))
        self.assertTrue(self.response.context['flash'].is_active_empty())
        
        self.response = self.client.get(reverse(views.render_template))
        self.assertEqual('Oops', self.response.context['flash']['message'])
        
        self.response = self.client.get(reverse(views.render_template))
        self.assertTrue(self.response.context['flash'].is_active_empty())
    
    def test_variable_lifecycle(self):
        "Test flash context management with one variable."
        self.response = self.client.get(reverse(views.variable_lifecycle))
        self.response = self.client.get(reverse(views.render_template))
        
        self.assertEqual('Something funny', self.response.context['flash']['message'])
        
        self.response = self.client.get(reverse(views.render_template))
        self.assertTrue(self.response.context['flash'].is_active_empty())
    
    def test_several_variables_lifecycle(self):
        "Test flash context management with two variables in several requests."
        self.response = self.client.get(reverse(views.several_variables_lifecycle))
        self.response = self.client.get(reverse(views.variable_lifecycle))
        self.assertEqual('Something else', self.response.context['flash']['another_message'])
        self.assertFalse(self.response.context['flash'].has_key('message'))
        
        self.response = self.client.get(reverse(views.render_template))
        self.assertEqual('Something funny', self.response.context['flash']['message'])
        self.assertFalse(self.response.context['flash'].has_key('another_message'))
        
        self.response = self.client.get(reverse(views.render_template))
        self.assertTrue(self.response.context['flash'].is_active_empty())
    
    def test_keep_variables(self):
        "Keep a flash scoped object for one more request."
        self.response = self.client.get(reverse(views.variable_lifecycle))
        
        for num in range(3):
            self.response = self.client.get(reverse(views.keep_variables))
            self.assertEqual('Something funny', self.response.context['flash']['message'])
        
        self.response = self.client.get(reverse(views.render_template))
        self.assertEqual('Something funny', self.response.context['flash']['message'])
        
        self.response = self.client.get(reverse(views.render_template))
        self.assertTrue(self.response.context['flash'].is_active_empty())
    
    def test_keep_invalid_variables(self):
        "Try to keep an invalid flash scoped object for one more request."
        self.response = self.client.get(reverse(views.variable_lifecycle))
        
        self.response = self.client.get(reverse(views.keep_invalid_variables))
        self.assertEqual('Something funny', self.response.context['flash']['message'])
        
        self.response = self.client.get(reverse(views.render_template))
        self.assertTrue(self.response.context['flash'].is_active_empty())
    
    def test_keep_all_variables(self):
        "Keep all flash scoped objects for one more request."
        self.response = self.client.get(reverse(views.variable_lifecycle))
        
        for num in range(3):
            self.response = self.client.get(reverse(views.keep_all_variables))
            self.assertEqual('Something funny', self.response.context['flash']['message'])
        
        self.response = self.client.get(reverse(views.render_template))
        self.assertEqual('Something funny', self.response.context['flash']['message'])
        
        self.response = self.client.get(reverse(views.render_template))
        self.assertTrue(self.response.context['flash'].is_active_empty())
