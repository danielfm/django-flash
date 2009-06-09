# -*- coding: utf-8 -*-

"""Integration test cases.
"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from djangoflash.context_processors import CONTEXT_VAR
from djangoflash.middleware import FlashMiddleware

from testproj.app import views


class IntegrationTestCase(TestCase):
    """Test the middleware and the context processors working within a real
    Django application.
    """
    def _flash(self):
        """Shortcut to get the flash scope from the view context.
        """
        return self.response.context[CONTEXT_VAR]

    def test_session_state_for_unused_flash(self):
        """Flash scope shouldn't be stored in the session if there's no flash.
        """
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse(FlashMiddleware._SESSION_KEY in self.client.session)

    def test_session_state_for_used_flash(self):
        """Flash scope should be removed from the session if there's no flash.
        """
        self.response = self.client.get(reverse(views.set_flash_var))
        self.response = self.client.get(reverse(views.render_template))
        self.assertTrue(FlashMiddleware._SESSION_KEY in self.client.session)

        # Flash scope should be removed from the session
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse(FlashMiddleware._SESSION_KEY in self.client.session)

    def test_default_lifecycle(self):
        """A value should be automatically removed from the flash scope.
        """
        self.response = self.client.get(reverse(views.set_flash_var))
        self.assertEqual('Message', self._flash()['message'])

        self.response = self.client.get(reverse(views.render_template))
        self.assertEqual('Message', self._flash()['message'])

        # Flash value will be removed when this request hits the app
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())

    def test_keep_lifecycle(self):
        """A value shouldn't be removed from the flash scope when it is kept.
        """
        self.response = self.client.get(reverse(views.set_flash_var))
        self.assertEqual('Message', self._flash()['message'])

        self.response = self.client.get(reverse(views.keep_var))
        self.assertEqual('Message', self._flash()['message'])

        # Flash value won't be removed now because it was explicitely kept
        self.response = self.client.get(reverse(views.render_template))
        self.assertEqual('Message', self._flash()['message'])

        # Flash value will be removed when this request hits the app
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())

    def test_now_lifecycle(self):
        """An immediate value shouldn't survive the next request.
        """
        self.response = self.client.get(reverse(views.set_now_var))
        self.assertEqual('Message', self._flash()['message'])

        # Flash value will be removed when this request hits the app
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())

    def test_discard_lifecycle(self):
        """A discarded value shouldn't survive to the next request.
        """
        self.response = self.client.get(reverse(views.discard_var))
        self.assertEqual('Message', self._flash()['message'])

        # Flash value will be removed when this request hits the app
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())

    def test_multiple_variables_lifecycle(self):
        """The flash scope should control several values independently.
        """
        self.response = self.client.get(reverse(views.set_flash_var))
        self.assertEqual('Message', self._flash()['message'])

        self.response = self.client.get(reverse(views.set_another_flash_var))
        self.assertEqual('Message', self._flash()['message'])
        self.assertEqual('Another message', self._flash()['anotherMessage'])

        # 'message' will be removed when this request hits the app
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())
        self.assertEqual('Another message', self._flash()['anotherMessage'])

        # 'anotherMessage' will be removed when this request hits the app
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())
        self.assertFalse('anotherMessage' in self._flash())

    def test_replace_flash_scope(self):
        """The flash scope should be an instance of FlashScope.
        """
        request = lambda: self.client.get(reverse(views.replace_flash))
        self.assertRaises(TypeError, request)

    def test_remove_flash_scope(self):
        """The app should not break even if request.flash doesn't exists.
        """
        self.response = self.client.get(reverse(views.remove_flash))
        self.assertFalse(self._flash() is None)
