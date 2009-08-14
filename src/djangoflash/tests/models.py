# -*- coding: utf-8 -*-

"""djangoflash.models test cases.
"""

from unittest import TestCase

from djangoflash.models import FlashScope


# Only exports test cases
__all__ = ['FlashScopeTestCase']


class FlashScopeTestCase(TestCase):
    """Tests the FlashScope object.
    """
    def setUp(self):
        """Create a FlashScope object to be used by the test methods.
        """
        self.flash = FlashScope()
        self.flash['message'] = 'Message'

    def test_contains(self):
        """FlashScope: "key in flash" syntax should be supported.
        """
        self.assertFalse('another_message' in self.flash)
        self.assertTrue('message' in self.flash)

    def test_get_item(self):
        """FlashScope: flash[key]" syntax should be supported.
        """
        self.assertRaises(KeyError, lambda: self.flash['another_message']);
        self.assertEqual('Message', self.flash['message']);

    def test_set_item(self):
        """FlashScope: flash[key] = value" syntax should be supported.
        """
        self.flash['another_message'] = 'Another message'
        self.assertEqual('Another message', self.flash['another_message']);

    def test_del_item(self):
        """FlashScope: "del flash[key]" syntax should be supported.
        """
        self.assertEqual('Message', self.flash['message'])
        del self.flash['message']
        self.assertFalse('message' in self.flash)

    def test_clear(self):
        """FlashScope: flash.clear() should remove all items from the flash scope.
        """
        self.flash['anotherMessage'] = 'Another message'
        self.assertEqual(2, len(self.flash))
        self.flash.clear()
        self.assertEqual(0, len(self.flash))

    def test_len(self):
        """FlashScope: "len(flash)" syntax should be supported.
        """
        self.assertEqual(1, len(self.flash))

    def test_keys(self):
        """FlashScope: Should return the list of keys stored in the flash scope.
        """
        self.assertEqual(['message'], self.flash.keys())

    def test_values(self):
        """FlashScope: Should return the list of values stored in the flash scope.
        """
        self.assertEqual(['Message'], self.flash.values())

    def test_items(self):
        """FlashScope: Should return the list of items stored in the flash scope.
        """
        self.assertEqual([('message', 'Message')], self.flash.items())

    def test_iterkeys(self):
        """FlashScope: Should return an iterator to the keys stored in the flash scope.
        """
        iterator = self.flash.iterkeys()
        self.assertEqual('message', iterator.next())
        self.assertRaises(StopIteration, iterator.next)

    def test_itervalues(self):
        """FlashScope: Should return an iterator to the values stored in the flash scope.
        """
        iterator = self.flash.itervalues()
        self.assertEqual('Message', iterator.next())
        self.assertRaises(StopIteration, iterator.next)

    def test_iteritems(self):
        """FlashScope: Should return an iterator to the items stored in the flash scope.
        """
        iterator = self.flash.iteritems()
        self.assertEqual(('message', 'Message'), iterator.next())
        self.assertRaises(StopIteration, iterator.next)

    def test_add_with_existing_non_list_value(self):
        """FlashScope: Should add values to a key even if the current value is not a list.
        """
        self.flash.add('message', 'Another Message')
        self.assertEqual(['Message', 'Another Message'], self.flash['message'])

    def test_add_with_existing_list_value(self):
        """FlashScope: Should add a new value if the current value is a list.
        """
        self.flash['another_message'] = ['Message 1']
        self.flash.add('another_message', 'Message 2')
        self.assertEqual(['Message 1', 'Message 2'], self.flash['another_message'])

    def test_add_with_no_existing_value(self):
        """FlashScope: Should add a value even if the given key doesn't exists.
        """
        self.flash.add('another_message', 'Another Message')
        self.assertEqual(['Another Message'], self.flash['another_message'])

    def test_get(self):
        """FlashScope: Should return a default value if the given key doesn' exists.
        """
        self.assertEqual('Oops', self.flash.get('another_message', 'Oops'))
        self.assertEqual('Message', self.flash.get('message', 'Something'))
        self.assertEqual(None, self.flash.get('another_message'))

    def test_pop(self):
        """FlashScope: Should pop an item from the flash scope.
        """
        self.assertEqual(None,self.flash.pop('another_message'))
        self.assertEqual('Message', self.flash.pop('message'))
        self.assertFalse('message' in self.flash)

    def test_pop_used_value(self):
        """FlashScope: Should pop an used item from the flash scope.
        """
        self.flash.update()
        self.assertEqual('Message', self.flash.pop('message'))
        self.assertFalse('message' in self.flash)

    def test_has_key(self):
        """FlashScope: Should check if there's a value related with the given key.
        """
        self.assertFalse(self.flash.has_key('another_message'))
        self.assertTrue(self.flash.has_key('message'))

    def test_put(self):
        """FlashScope: Should put several values into the flash scope at the same time.
        """
        self.flash.put(msg1='Message1', msg2='Message2')
        self.assertEqual('Message1', self.flash['msg1'])
        self.assertEqual('Message2', self.flash['msg2'])

    def test_discard(self):
        """FlashScope: Should mark a flash-scoped value for removal.
        """
        self.flash.discard()
        self.flash.update()
        self.assertFalse('message' in self.flash)

    def test_keep(self):
        """FlashScope: Should avoid the removal of specific flash-scoped values.
        """
        self.flash.update()
        self.flash.keep('message')
        self.flash.update()
        self.assertEqual('Message', self.flash['message'])
        self.flash.update()
        self.assertFalse('message' in self.flash)

    def test_keep_all(self):
        """FlashScope: Should avoid the removal of all flash-scoped values.
        """
        self.flash.update()
        self.flash.keep()
        self.flash.update()
        self.assertEqual('Message', self.flash['message'])
        self.flash.update()
        self.assertFalse('message' in self.flash)

    def test_alternative_now(self):
        """FlashScope: Immediate values (flash.now) should be supported.
        """
        self.flash.now(another_message='Another message')
        self.assertEqual('Another message', self.flash['another_message'])
        self.flash.update()
        self.assertFalse('another_message' in self.flash)

    def test_now(self):
        """FlashScope: "flash.now[key] = value" syntax should be supported.
        """
        self.flash.now['another_message'] = 'Another message'
        self.assertEqual('Another message', self.flash['another_message'])
        self.flash.update()
        self.assertFalse('another_message' in self.flash)

    def test_now_get_item(self):
        """FlashScope: "FlashScope: "flash.now[key]" syntax should be supported.
        """
        self.flash.now['another_message'] = 'Another message'
        self.assertEqual('Another message', self.flash.now['another_message'])

    def test_now_contains(self):
        """FlashScope: "key in flash.now" syntax should be supported.
        """
        self.assertFalse('another_message' in self.flash.now)
        self.flash.now['another_message'] = 'Another message'
        self.assertTrue('another_message' in self.flash.now)

    def test_replace_value(self):
        """FlashScope: Should replace a value properly.
        """
        self.flash['message'] = 'Message'
        self.flash.update()
        self.assertEqual('Message', self.flash['message'])
        self.flash['message'] = 'Another Message'
        self.assertEqual('Another Message', self.flash['message'])
        self.flash.update()
        self.assertEqual('Another Message', self.flash['message'])
        self.flash.update()
        self.assertFalse('message' in self.flash)

    def test_replace_with_immediage_value(self):
        """FlashScope: Should replace a value properly by a immediate value.
        """
        self.flash['message'] = 'Message'
        self.flash.update()
        self.assertEqual('Message', self.flash['message'])
        self.flash.now['message'] = 'Another Message'
        self.assertEqual('Another Message', self.flash['message'])
        self.flash.update()
        self.assertFalse('message' in self.flash)
