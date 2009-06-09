# -*- coding: utf-8 -*-

"""djangoflash.models test cases.
"""

from unittest import TestCase

from djangoflash.middleware import FlashScope


class FlashScopeTestCase(TestCase):
    """Test the FlashScope object.
    """
    def setUp(self):
        """Create a FlashScope object to be used by the test methods.
        """
        self.scope = FlashScope()
    
    def test_contains(self):
        """"key in flash" syntax should be supported.
        """
        self.assertFalse('message' in self.scope)
        self.scope['message'] = 'Message'
        self.assertTrue('message' in self.scope)
    
    def test_get_item(self):
        """"flash[key]" syntax should be supported.
        """
        get_item = lambda: self.scope['message']
        self.assertRaises(KeyError, get_item);
        self.scope['message'] = 'Message'
        self.assertEqual('Message', get_item());
        
    
    def test_set_item(self):
        """"flash[key] = value" syntax should be supported.
        """
        self.scope['message'] = 'Message'
        self.assertEqual('Message', self.scope['message']);
    
    def test_del_item(self):
        """"del flash[key]" syntax should be supported.
        """
        self.scope['message'] = 'Message'
        del self.scope['message']
        self.assertFalse('message' in self.scope)
    
    def test_clear(self):
        """flash.clear() should remove all items from the flash scope.
        """
        self.scope['message'] = 'Message'
        self.scope['anotherMessage'] = 'Another message'
        self.scope.clear()
        self.assertEqual(0, len(self.scope))
    
    def test_len(self):
        """"len(flash)" syntax should be supported.
        """
        self.scope['message'] = 'Message'
        self.assertEqual(1, len(self.scope))
    
    def test_keys(self):
        """Should return the list of keys stored in the flash scope.
        """
        self.scope['message'] = 'Message'
        self.assertEqual(['message'], self.scope.keys())
    
    def test_values(self):
        """Should return the list of values stored in the flash scope.
        """
        self.scope['message'] = 'Message'
        self.assertEqual(['Message'], self.scope.values())
    
    def test_items(self):
        """Should return the list of items stored in the flash scope.
        """
        self.scope['message'] = 'Message'
        self.assertEqual([('message', 'Message')], self.scope.items())
    
    def test_iterkeys(self):
        """Should return an iterator to the keys stored in the flash scope.
        """
        self.scope['message'] = 'Message'
        iterator = self.scope.iterkeys()
        self.assertEqual('message', iterator.next())
        self.assertRaises(StopIteration, iterator.next)
    
    def test_itervalues(self):
        """Should return an iterator to the values stored in the flash scope.
        """
        self.scope['message'] = 'Message'
        iterator = self.scope.itervalues()
        self.assertEqual('Message', iterator.next())
        self.assertRaises(StopIteration, iterator.next)
    
    def test_iteritems(self):
        """Should return an iterator to the items stored in the flash scope.
        """
        self.scope['message'] = 'Message'
        iterator = self.scope.iteritems()
        self.assertEqual(('message', 'Message'), iterator.next())
        self.assertRaises(StopIteration, iterator.next)
    
    def test_get(self):
        """Should return a default value if the given key doesn' exists.
        """
        self.assertEqual('Something', self.scope.get('message', 'Something'))
        self.scope['message'] = 'Message'
        self.assertEqual('Message', self.scope.get('message', 'Something'))
        self.assertEqual(None, self.scope.get('another_message'))
    
    def test_pop(self):
        """Should pop an item from the flash scope.
        """
        self.assertEqual(None,self.scope.pop('message'))
        self.scope['message'] = 'Message'
        self.assertEqual('Message', self.scope.pop('message'))
        self.assertFalse('message' in self.scope)
    
    def test_pop_used_value(self):
        """Should pop an used item from the flash scope.
        """
        self.scope['message'] = 'Message'
        self.scope.update()
        self.assertEqual('Message', self.scope.pop('message'))
        self.assertFalse('message' in self.scope)
    
    def test_has_key(self):
        """Should check if there's a value related with the given key.
        """
        self.assertFalse(self.scope.has_key('message'))
        self.scope['message'] = 'Message'
        self.assertTrue(self.scope.has_key('message'))
    
    def test_put(self):
        """Should put several values into the flash scope at the same time.
        """
        self.scope.put(msg1='Message1', msg2='Message2')
        self.assertEqual('Message1', self.scope['msg1'])
        self.assertEqual('Message2', self.scope['msg2'])
    
    def test_discard(self):
        """Should mark a flash-scoped value for removal.
        """
        self.scope['message'] = 'Message'
        self.scope.discard()
        
        self.scope.update()
        self.assertFalse('message' in self.scope)
    
    def test_keep(self):
        """Should mark all flash-scoped value for removal.
        """
        self.scope['message'] = 'Message'
        self.scope.update()
        self.scope.keep('message')
        self.scope.update()
        self.assertEqual('Message', self.scope['message'])
    
    def test_keep_all(self):
        """Should avoid the removal of all flash-scoped values.
        """
        self.scope['message'] = 'Message'
        self.scope.update()
        self.scope.keep()
        self.scope.update()
        self.assertEqual('Message', self.scope['message'])
    
    def test_alternative_now(self):
        """Immediate values (flash.now) should be supported.
        """
        self.scope.now(message='Message')
        self.assertEqual('Message', self.scope['message'])
        self.scope.update()
        self.assertFalse('message' in self.scope)
    
    def test_now(self):
        """"flash.now[key] = value" syntax should be supported.
        """
        self.scope.now['message'] = 'Message'
        self.assertEqual('Message', self.scope['message'])
        self.scope.update()
        self.assertFalse('message' in self.scope)
    
    def test_now_get_item(self):
        """"flash.now[key]" syntax should be supported.
        """
        self.scope.now['message'] = 'Message'
        self.assertEqual('Message', self.scope.now['message'])
    
    def test_now_contains(self):
        """"key in flash.now" syntax should be supported.
        """
        self.assertFalse('message' in self.scope.now)
        self.scope.now['message'] = 'Message'
        self.assertTrue('message' in self.scope.now)
