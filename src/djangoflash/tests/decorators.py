# -*- coding: utf-8 -*-

"""djangoflash.decorators test cases.
"""

from unittest import TestCase

from django.http import HttpRequest

from djangoflash.decorators import keep_messages
from djangoflash.models import FlashScope


# Only exports test cases
__all__ = ['KeepMessagesDecoratorTestCase']


def view_method(request):
    """Function that simulates a Django view.
    """
    if hasattr(request, 'flash'):
        request.flash.update()
        return True
    return False


class KeepMessagesDecoratorTestCase(TestCase):
    """Tests the keep_messages decorator.
    """
    def setUp(self):
        """Create a request with an used message inside the flash.
        """
        self.request = HttpRequest()
        self.request.flash = self.flash = FlashScope()
        self.flash['message'] = 'Message'
        self.flash.update()

    def test_decorator_with_no_flash(self):
        """Decorators: keep_messages should not break when there's no flash scope attached to the request.
        """
        self.request = HttpRequest()
        view = keep_messages(view_method)
        self.assertFalse(view(self.request))

    def test_decorator_with_no_args(self):
        """Decorators: keep_messages with no args should avoid the removal of all flash-scoped values. 
        """
        view = keep_messages(view_method)
        self.assertEqual('Message', self.flash['message'])

        self.assertTrue(view(self.request))
        self.assertEqual('Message', self.flash['message'])

        view_method(self.request)
        self.assertFalse('message' in self.flash)

    def test_decorator_with_empty_args(self):
        """Decorators: keep_messages with empty args should avoid the removal of all flash-scoped values. 
        """
        view = keep_messages()(view_method)
        self.assertEqual('Message', self.flash['message'])

        self.assertTrue(view(self.request))
        self.assertEqual('Message', self.flash['message'])

        view_method(self.request)
        self.assertFalse('message' in self.flash)

    def test_decorator_with_args(self):
        """Decorators: keep_messages should avoid the removal of specific flash-scoped values.
        """
        view = keep_messages('message', 'another_message')(view_method)
        self.assertEqual('Message', self.flash['message'])

        self.assertTrue(view(self.request))
        self.assertEqual('Message', self.flash['message'])

        view_method(self.request)
        self.assertFalse('message' in self.flash)

    def test_decorator_with_invalid_arg(self):
        """Decorators: keep_messages should not avoid the removal of flash-scoped values.
        """
        view = keep_messages('another_message')(view_method)
        self.assertEqual('Message', self.flash['message'])

        self.assertTrue(view(self.request))
        self.assertFalse('message' in self.flash)
