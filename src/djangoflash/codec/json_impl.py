# -*- coding: utf-8 -*-

"""This module provides a JSON-based codec implementation.
"""

try:
    import json 
except ImportError:
    from django.utils import simplejson as json

from djangoflash.codec import BaseCodec
from djangoflash.models import FlashScope


class CodecClass(BaseCodec):
    """JSON-based codec implementation.
    """
    def __init__(self):
        """Returns a new JSON-based codec.
        """
        BaseCodec.__init__(self)

    def encode(self, flash):
        """Encodes the given *flash* as a JSON string.
        """
        return json.dumps(flash.to_dict())

    def decode(self, encoded_flash):
        """Restores the *flash* from the given JSON string.
        """
        return FlashScope(json.loads(encoded_flash))
