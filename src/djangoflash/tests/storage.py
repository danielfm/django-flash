# -*- coding: utf-8 -*-

"""djangoflash.storage test cases.
"""

from unittest import TestCase

from django.http import HttpRequest, HttpResponse

from djangoflash.models import FlashScope
import djangoflash.storage as flash_storage
import djangoflash.storage.session as session_storage
import djangoflash.storage.cookie as cookie_storage


class StorageTestCase(TestCase):
    """Tests methods used to parse flash storage URIs and create flash storage
    objects.
    """
    def test_get_session_storage_by_relative_name(self):
        """'session' should resolve to session flash storage.
        """
        self.assertTrue(isinstance(flash_storage.get_storage('session'), \
            session_storage.FlashStorageClass))

    def test_get_cookie_storage_by_relative_name(self):
        """'cookie' should resolve to cookie flash storage.
        """
        self.assertTrue(isinstance(flash_storage.get_storage('cookie'), \
            cookie_storage.FlashStorageClass))

    def test_get_storage_by_module_name(self):
        """djangoflash.storage.cookie' should resolve to cookie flash storage.
        """
        self.assertTrue(isinstance(flash_storage.get_storage('djangoflash.storage.cookie'),
            cookie_storage.FlashStorageClass))


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
        self.storage = session_storage.FlashStorageClass()

    def test_set_null_object(self):
        """Session-based storage should not store null values.
        """
        self.storage.set(None, self.request, self.response)
        self.assertEqual(0, len(self.request.session))

    def test_set_empty_object(self):
        """Session-based storage should not store empty objects.
        """
        self.storage.set(self.flash, self.request, self.response)
        self.assertEqual(0, len(self.request.session))

    def test_set_object(self):
        """Session-based storage should store valid objects.
        """
        self.flash['message'] = 'Message'
        self.storage.set(self.flash, self.request, self.response)
        self.assertEqual(1, len(self.request.session))

    def test_get_empty(self):
        """Session-based storage should return nothing when empty.
        """
        self.assertEqual(None, self.storage.get(self.request))

    def test_get(self):
        """Session-based storage should return the stored object.
        """
        self.flash['message'] = 'Message'
        self.storage.set(self.flash, self.request, self.response)
        self.assertEqual(1, len(self.storage.get(self.request)))


class CookieFlashStorageTestCase(TestCase):
    """Tests the cookie-based flash storage class.
    """
    def setUp(self):
        """Creates a cookie-based flash storage for testing.
        """
        self.request = HttpRequest()
        self.response = HttpResponse('')
        self.flash = FlashScope()
        self.storage = cookie_storage.FlashStorageClass()

    def _transfer_cookies_from_response_to_request(self):
        """Transfers the cookies set in the response to the request.
        """
        for key, cookie in self.response.cookies.items():
            self.request.COOKIES[key] = cookie.value

    def test_set_null_object(self):
        """Cookie-based storage should not store null values.
        """
        self.storage.set(None, self.request, self.response)
        self.assertEqual(0, len(self.response.cookies))

    def test_set_empty_object(self):
        """Cookie-based storage should not store an empty object.
        """
        self.storage.set(self.flash, self.request, self.response)
        self.assertEqual(0, len(self.response.cookies))

    def test_set_object(self):
        """Cookie-based storage should store valid objects.
        """
        self.flash['message'] = 'Message'
        self.storage.set(self.flash, self.request, self.response)
        self.assertEqual(1, len(self.response.cookies))

    def test_get_empty(self):
        """Cookie-based storage should return nothing when empty.
        """
        self.assertEqual(None, self.storage.get(self.request))

    def test_get(self):
        """Cookie-based storage should return the stored object.
        """
        self.flash['message'] = 'Message'
        self.storage.set(self.flash, self.request, self.response)
        self.assertEqual(None, self.storage.get(self.request))

        self._transfer_cookies_from_response_to_request()
        self.assertEqual(1, len(self.storage.get(self.request)))
