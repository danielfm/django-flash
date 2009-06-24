# -*- coding: utf-8 -*-

"""This module provides a cookie-based flash storage backend.

.. warning::
   The actual :class:`FlashScope` object is sent back to the user inside a
   cookie. Although some encryption is performed to help spot when the flash
   data is modified by third-parties, this backend should be avoided when
   sensitive information is stored inside the *flash*.

.. warning::
   Although in general user agents' cookie support should have no fixed limits,
   according to `RFC-2965 <http://www.ietf.org/rfc/rfc2965.txt>`_, section 5.3,
   all implementations must support at least 4096 bytes per cookie. So be
   careful about the amount of data you store inside the *flash* when using
   this storage backend.
"""

from djangoflash.storage.base import BaseFlashStorage


class FlashStorageClass(BaseFlashStorage):
    """Cookie-based flash storage backend.
    """

    def __init__(self):
        """Returns a new cookie-based flash storage backend.
        """
        BaseFlashStorage.__init__(self)
        self._key = '_djflash_cookie'

    def set(self, flash, request, response):
        """Stores the given :class:`FlashScope` object.
        """
        if flash:
            response.set_cookie(self._key, self.encode(flash))
        elif self._key in request.COOKIES:
            response.delete_cookie(self._key)

    def get(self, request):
        """Returns the stored :class:`FlashScope` object.
        """
        data = request.COOKIES.get(self._key)
        if data:
            return self.decode(data)
