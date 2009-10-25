# -*- coding: utf-8 -*-

"""This module provides a Pickle-based codec implementation.

.. warning::
   The use of this codec is not recommended since the
   `Pickle documentation <http://docs.python.org/library/pickle.html>`_ itself
   clearly states that it's not intended to be secure against erroneous or
   maliciously constructed data.
"""

try:
    import cPickle as pickle
except ImportError:
    import pickle

from djangoflash.codec import BaseCodec


class CodecClass(BaseCodec):
    """Pickle-based codec implementation.
    """
    def __init__(self):
        """Returns a new Pickle-based codec.
        """
        BaseCodec.__init__(self)

    def encode(self, flash):
        """Encodes the given *flash* as a Pickle dump string.
        """
        return pickle.dumps(flash, pickle.HIGHEST_PROTOCOL)

    def decode(self, encoded_flash):
        """Restores the *flash* from the given Pickle dump string.
        """
        return pickle.loads(encoded_flash)
