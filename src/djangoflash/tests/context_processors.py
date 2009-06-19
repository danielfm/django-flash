# -*- coding: utf-8 -*-

"""djangoflash.context_processors test cases.
"""

from unittest import TestCase

from django.http import HttpRequest

from djangoflash.context_processors import CONTEXT_VAR, flash
from djangoflash.models import FlashScope


class FlashContextProcessorTestCase(TestCase):
    """Tests the flash context processor.
    """
    def setUp(self):
        self.request = HttpRequest()
        self.scope = FlashScope();
        setattr(self.request, CONTEXT_VAR, self.scope);

    def test_expose_flash_scope(self):
        """Context processor should expose the flash scope."""
        self.assertEqual(flash(self.request), {CONTEXT_VAR:self.scope})

    def test_expose_inexistent_flash_scope(self):
        """Context processor should expose a new flash scope when none is available."""
        delattr(self.request, CONTEXT_VAR)
        self.assertTrue(isinstance(flash(self.request)[CONTEXT_VAR], FlashScope))
