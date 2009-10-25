# -*- coding: utf-8 -*-

"""djangoflash.models test cases.
"""

from unittest import TestCase

from djangoflash.models import FlashScope, _SESSION_KEY, _USED_KEY


class FlashScopeTestCase(TestCase):
    """Tests the FlashScope object.
    """
    def setUp(self):
        """Create a FlashScope object to be used by the test methods.
        """
        self.flash = FlashScope()
        self.flash['info'] = 'Info'

    def test_restore(self):
        """FlashScope: Should restore the flash using a dict.
        """
        data = {_SESSION_KEY: {'info' : 'Info',
                               'error': 'Error'},
                _USED_KEY   : {'error': None}}
        self.flash = FlashScope(data)
        self.assertEqual(2, len(self.flash))
        self.assertEqual('Info', self.flash['info'])
        self.assertEqual('Error', self.flash['error'])
        self.flash.update()
        self.assertEqual('Info', self.flash['info'])
        self.assertFalse('error' in self.flash)

    def test_restore_immutability(self):
        """FlashScope: Should restore the flash using a shallow copy of a dict.
        """
        data = {_SESSION_KEY: {'info' : 'Info',
                               'error': 'Error'},
                _USED_KEY   : {'error': None}}
        self.flash = FlashScope(data)
        self.assertEqual('Info', self.flash['info'])
        del data[_SESSION_KEY]['info']
        self.assertTrue('info' in self.flash)

    def test_restore_with_invalid_type(self):
        """FlashScope: Should not restore the flash using an invalid object.
        """
        self.assertRaises(TypeError, lambda: FlashScope('invalid_data'))

    def test_restore_with_invalid_keys(self):
        """FlashScope: Should not restore the flash using a dict with invalid keys.
        """
        data = {_SESSION_KEY: None}
        self.assertRaises(ValueError, lambda: FlashScope(data))
        data = {_USED_KEY: None}
        self.assertRaises(ValueError, lambda: FlashScope(data))

    def test_restore_with_invalid_values(self):
        """FlashScope: Should not restore the flash using a dict with invalid values.
        """
        data = {_SESSION_KEY: {}, _USED_KEY: None}
        self.assertRaises(ValueError, lambda: FlashScope(data))
        data = {_SESSION_KEY: None, _USED_KEY: {}}
        self.assertRaises(ValueError, lambda: FlashScope(data))

    def test_contains(self):
        """FlashScope: "key in flash" syntax should be supported.
        """
        self.assertFalse('error' in self.flash)
        self.assertEqual('Info', self.flash['info'])

    def test_get_item(self):
        """FlashScope: flash[key]" syntax should be supported.
        """
        self.assertRaises(KeyError, lambda: self.flash['error']);
        self.assertEqual('Info', self.flash['info']);

    def test_set_item(self):
        """FlashScope: flash[key] = value" syntax should be supported.
        """
        self.flash['error'] = 'Error'
        self.assertEqual('Error', self.flash['error']);

    def test_del_item(self):
        """FlashScope: "del flash[key]" syntax should be supported.
        """
        self.assertEqual('Info', self.flash['info'])
        del self.flash['info']
        self.assertFalse('info' in self.flash)

    def test_clear(self):
        """FlashScope: flash.clear() should remove all items from the flash scope.
        """
        self.flash['error'] = 'Error'
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
        self.assertEqual(['info'], self.flash.keys())

    def test_values(self):
        """FlashScope: Should return the list of values stored in the flash scope.
        """
        self.assertEqual(['Info'], self.flash.values())

    def test_items(self):
        """FlashScope: Should return the list of items stored in the flash scope.
        """
        self.assertEqual([('info', 'Info')], self.flash.items())

    def test_iterkeys(self):
        """FlashScope: Should return an iterator to the keys stored in the flash scope.
        """
        iterator = self.flash.iterkeys()
        self.assertEqual('info', iterator.next())
        self.assertRaises(StopIteration, iterator.next)

    def test_itervalues(self):
        """FlashScope: Should return an iterator to the values stored in the flash scope.
        """
        iterator = self.flash.itervalues()
        self.assertEqual('Info', iterator.next())
        self.assertRaises(StopIteration, iterator.next)

    def test_iteritems(self):
        """FlashScope: Should return an iterator to the items stored in the flash scope.
        """
        iterator = self.flash.iteritems()
        self.assertEqual(('info', 'Info'), iterator.next())
        self.assertRaises(StopIteration, iterator.next)

    def test_add_with_existing_non_list_value(self):
        """FlashScope: Should add values to a key even if the current value is not a list.
        """
        self.flash.add('info', 'Error')
        self.assertEqual(['Info', 'Error'], self.flash['info'])

    def test_add_with_existing_list_value(self):
        """FlashScope: Should add a new value if the current value is a list.
        """
        self.flash['error'] = ['Error 1']
        self.flash.add('error', 'Error 2')
        self.assertEqual(['Error 1', 'Error 2'], self.flash['error'])

    def test_add_with_no_existing_value(self):
        """FlashScope: Should add a value even if the given key doesn't exists.
        """
        self.flash.add('error', 'Error')
        self.assertEqual(['Error'], self.flash['error'])

    def test_get(self):
        """FlashScope: Should return a default value if the given key doesn' exists.
        """
        self.assertEqual('Oops', self.flash.get('error', 'Oops'))
        self.assertEqual('Info', self.flash.get('info', 'Something'))
        self.assertEqual(None, self.flash.get('error'))

    def test_pop(self):
        """FlashScope: Should pop an item from the flash scope.
        """
        self.assertEqual(None, self.flash.pop('error'))
        self.assertEqual('Info', self.flash.pop('info'))
        self.assertFalse('info' in self.flash)

    def test_pop_used_value(self):
        """FlashScope: Should pop an used item from the flash scope.
        """
        self.flash.update()
        self.assertEqual('Info', self.flash.pop('info'))
        self.assertFalse('info' in self.flash)

    def test_has_key(self):
        """FlashScope: Should check if there's a value related with the given key.
        """
        self.assertFalse(self.flash.has_key('error'))
        self.assertTrue(self.flash.has_key('info'))

    def test_put(self):
        """FlashScope: Should put several values into the flash scope at the same time.
        """
        self.flash.put(warn='Warning', error='Error')
        self.assertEqual('Warning', self.flash['warn'])
        self.assertEqual('Error', self.flash['error'])

    def test_discard(self):
        """FlashScope: Should mark a flash-scoped value for removal.
        """
        self.flash.discard()
        self.flash.update()
        self.assertFalse('info' in self.flash)

    def test_keep(self):
        """FlashScope: Should avoid the removal of specific flash-scoped values.
        """
        self.flash.update()
        self.flash.keep('info')
        self.flash.update()
        self.assertEqual('Info', self.flash['info'])
        self.flash.update()
        self.assertFalse('info' in self.flash)

    def test_keep_all(self):
        """FlashScope: Should avoid the removal of all flash-scoped values.
        """
        self.flash.update()
        self.flash.keep()
        self.flash.update()
        self.assertEqual('Info', self.flash['info'])
        self.flash.update()
        self.assertFalse('info' in self.flash)

    def test_alternative_now(self):
        """FlashScope: Immediate values (flash.now) should be supported.
        """
        self.flash.now(error='Error')
        self.assertEqual('Error', self.flash['error'])
        self.flash.update()
        self.assertFalse('error' in self.flash)

    def test_now(self):
        """FlashScope: "flash.now[key] = value" syntax should be supported.
        """
        self.flash.now['error'] = 'Error'
        self.assertEqual('Error', self.flash['error'])
        self.flash.update()
        self.assertFalse('error' in self.flash)

    def test_now_get_item(self):
        """FlashScope: "FlashScope: "flash.now[key]" syntax should be supported.
        """
        self.flash.now['error'] = 'Error'
        self.assertEqual('Error', self.flash.now['error'])

    def test_now_contains(self):
        """FlashScope: "key in flash.now" syntax should be supported.
        """
        self.assertFalse('error' in self.flash.now)
        self.flash.now['error'] = 'Error'
        self.assertTrue('error' in self.flash.now)

    def test_replace_value(self):
        """FlashScope: Should replace a value properly.
        """
        self.flash.update()
        self.assertEqual('Info', self.flash['info'])
        self.flash['info'] = 'Error'
        self.assertEqual('Error', self.flash['info'])
        self.flash.update()
        self.assertEqual('Error', self.flash['info'])
        self.flash.update()
        self.assertFalse('info' in self.flash)

    def test_replace_with_immediage_value(self):
        """FlashScope: Should replace a value properly by a immediate value.
        """
        self.flash.update()
        self.assertEqual('Info', self.flash['info'])
        self.flash.now['info'] = 'Error'
        self.assertEqual('Error', self.flash['info'])
        self.flash.update()
        self.assertFalse('info' in self.flash)

    def test_empty_to_dict(self):
        """FlashScope: Should export the flash data to a dict even if it's empty.
        """
        self.flash = FlashScope()
        expected_data = {_SESSION_KEY: {}, _USED_KEY:{}}
        data = self.flash.to_dict()
        self.assertEqual(expected_data, data)

    def test_to_dict(self):
        """FlashScope: Should export the flash data to a dict.
        """
        self.flash.update()
        self.flash['error'] = 'Error'
        expected_data = {_SESSION_KEY: {'info' : 'Info',
                                        'error': 'Error'},
                         _USED_KEY   : {'info' : None}}
        data = self.flash.to_dict()
        self.assertEqual(expected_data, data)

    def test_to_dict_immutability(self):
        """FlashScope: Should export a copy of the flash data as a dict.
        """
        data = self.flash.to_dict()
        del self.flash['info']
        self.assertEqual('Info', data[_SESSION_KEY]['info'])
