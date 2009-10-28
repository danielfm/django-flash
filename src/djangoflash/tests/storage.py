# -*- coding: utf-8 -*-

"""djangoflash.storage test cases.
"""

from unittest import TestCase

from django.http import HttpRequest, HttpResponse

from djangoflash.models import FlashScope
from djangoflash import storage
from djangoflash.storage import session, cookie


class StorageTestCase(TestCase):
    """Tests methods used to parse flash storage URIs and create flash storage
    objects.
    """
    def test_get_session_storage_by_alias(self):
        """Storage: 'session' should resolve to session flash storage.
        """
        storage_impl = storage.get_storage('session')
        self.assertTrue(isinstance(storage_impl, session.FlashStorageClass))

    def test_get_cookie_storage_by_alias(self):
        """Storage: 'cookie' should resolve to cookie flash storage.
        """
        storage_impl = storage.get_storage('cookie')
        self.assertTrue(isinstance(storage_impl, cookie.FlashStorageClass))

    def test_get_storage_by_module_name(self):
        """Storage: 'djangoflash.storage.cookie' should resolve to cookie flash storage.
        """
        storage_impl = storage.get_storage('djangoflash.storage.cookie')
        self.assertTrue(isinstance(storage_impl, cookie.FlashStorageClass))

    def test_get_storage_by_invalid_module_name(self):
        """Storage: Should raise an error when resolving a module name that doesn't exists.
        """
        operation = lambda: storage.get_storage('invalid.module.path')
        self.assertRaises(ImportError, operation)

    def test_get_storage_by_invalid_module(self):
        """Storage: Should raise an error when module doesn't provide a storage class.
        """
        operation = lambda: storage.get_storage('djangoflash.models')
        self.assertRaises(AttributeError, operation)


class SessionFlashStorageTestCase(TestCase):
    """Tests the session-based flash storage class.
    """
    def setUp(self):
        """Creates a cookie-based flash storage for testing.
        """
        self.request = HttpRequest()
        self.request.session = {}
        self.response = HttpResponse('')
        self.flash = FlashScope()
        self.storage = session.FlashStorageClass()

    def _get_flash(self):
        """Returns the flash contents from the session.
        """
        return self.request.session[self.storage._key]

    def test_set_null_object(self):
        """SessionStorage: should not store null values.
        """
        self.storage.set(None, self.request, self.response)
        self.assertEqual(0, len(self.request.session))

    def test_set_empty_object(self):
        """SessionStorage: should not store empty objects.
        """
        self.storage.set(self.flash, self.request, self.response)
        self.assertEqual(0, len(self.request.session))

    def test_clear_storage(self):
        """SessionStorage: should remove flash contents from the session.
        """
        self.flash['message'] = 'Message'
        self.storage.set(self.flash, self.request, self.response)
        self.assertEqual('Message', self._get_flash()['message'])

        # The flash should be completely removed from the session
        del self.flash['message']
        self.storage.set(self.flash, self.request, self.response)
        self.assertRaises(KeyError, self._get_flash)

    def test_set_object(self):
        """Session storage: should store valid objects.
        """
        self.flash['message'] = 'Message'
        self.storage.set(self.flash, self.request, self.response)
        self.assertEqual(1, len(self.request.session))

    def test_get_empty(self):
        """SessionStorage: should return nothing when empty.
        """
        self.assertEqual(None, self.storage.get(self.request))

    def test_get(self):
        """SessionStorage: should return the stored object.
        """
        self.flash['message'] = 'Message'
        self.storage.set(self.flash, self.request, self.response)
        self.assertEqual('Message', self.storage.get(self.request)['message'])


class CookieFlashStorageTestCase(TestCase):
    """Tests the cookie-based flash storage class.
    """
    def setUp(self):
        """Creates a cookie-based flash storage for testing.
        """
        self.request = HttpRequest()
        self.response = HttpResponse('')
        self.flash = FlashScope()
        self.storage = cookie.FlashStorageClass()

    def _transfer_cookies_from_response_to_request(self):
        """Transfers the cookies set in the response to the request.
        """
        for key, cookie in self.response.cookies.items():
            self.request.COOKIES[key] = cookie.value

    def _get_cookie(self):
        """Returns the cookie used to store the flash contents.
        """
        return self.response.cookies[self.storage._key]

    def test_set_null_object(self):
        """CookieStorage: should not store null values.
        """
        self.storage.set(None, self.request, self.response)
        self.assertEqual(0, len(self.response.cookies))

    def test_set_empty_object(self):
        """CookieStorage: should not store an empty object.
        """
        self.storage.set(self.flash, self.request, self.response)
        self.assertEqual(0, len(self.response.cookies))

    def test_clear_storage(self):
        """CookieStorage: should set an empty/expired cookie.
        """
        self.flash['message'] = 'Message'
        self.storage.set(self.flash, self.request, self.response)

        # Simulates a request-response cycle
        self._transfer_cookies_from_response_to_request()
        del self.flash['message']

        # Cookie should be empty/expired
        self.storage.set(self.flash, self.request, self.response)
        self.assertEqual(0, self._get_cookie()['max-age'])
        self.assert_(not self._get_cookie().value)

    def test_set_object(self):
        """CookieStorage: should store valid objects.
        """
        self.flash['message'] = 'Message'
        self.storage.set(self.flash, self.request, self.response)
        self.assertEqual(1, len(self.response.cookies))

    def test_get_empty(self):
        """CookieStorage: should return nothing when empty.
        """
        self.assertEqual(None, self.storage.get(self.request))

    def test_get(self):
        """CookieStorage: should return the stored object.
        """
        self.flash['message'] = 'Message'
        self.storage.set(self.flash, self.request, self.response)
        self.assertEqual(None, self.storage.get(self.request))

        # Simulates a request-response cycle
        self._transfer_cookies_from_response_to_request()
        self.assertEqual('Message', self.storage.get(self.request)['message'])
