# -*- coding: utf-8 -*-

"""This module provides the :class:`BaseFlashStorage` class, which can be
extended by custom flash storage backends.
"""

import base64

try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.conf import settings
from django.utils.hashcompat import md5_constructor


class BaseFlashStorage(object):
    """Base class that can be extended by custom flash storage backends.
    """

    def __init__(self):
        """Returns a new :class:`BaseFlashStorage` object.
        """
        pass

    def set(self, flash, request, response):
        """Stores the given :class:`FlashScope` object. Empty implementation
        that raises :class:`NotImplementedError`.
        """
        raise NotImplementedError

    def get(self, request):
        """Returns the stored :class:`FlashScope` object. Empty implementation
        that raises :class:`NotImplementedError`.
        """
        raise NotImplementedError

    def encode(self, data):
        """In order to serialize the given object, this method creates and
        returns a string containing a pickled-and-encoded version of the given
        object.
        """
        pickled = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        pickled_md5 = md5_constructor(pickled + settings.SECRET_KEY).hexdigest()
        return base64.encodestring(pickled + pickled_md5)

    def decode(self, data):
        """In order to recreate a serialized object from the given string, this
        method decodes-and-unpickles the given string and returns the resulting
        object.
        """
        encoded_data = base64.decodestring(data)
        pickled, tamper_check = encoded_data[:-32], encoded_data[-32:]
        hex_digest = md5_constructor(pickled + settings.SECRET_KEY).hexdigest()
        if hex_digest != tamper_check:
            from django.core.exceptions import SuspiciousOperation
            raise SuspiciousOperation("User tampered with session cookie.")
        try:
            return pickle.loads(pickled)
        # Unpickling can cause a variety of exceptions. If something happens,
        # just return None
        except:
            return None
