# -*- coding: utf-8 -*-

"""This module provides a JSON-based codec implementation that uses the
:mod:`zlib` module to reduce the encoded flash footprint.
"""

import zlib

from djangoflash.codec.json_impl import CodecClass as JSONCodecClass
from djangoflash.models import FlashScope


class CodecClass(JSONCodecClass):
    """JSON/zlib-based codec implementation.
    """
    def __init__(self):
        """Returns a new JSON/zlib-based codec.
        """
        JSONCodecClass.__init__(self)

    def encode(self, flash):
        """Encodes the given *flash* as a zlib compressed JSON string.
        """
        return zlib.compress(JSONCodecClass.encode(self, flash))

    def decode(self, encoded_flash):
        """Restores the *flash* from the given zlib compressed JSON string.
        """
        return JSONCodecClass.decode(self, zlib.decompress(encoded_flash))
