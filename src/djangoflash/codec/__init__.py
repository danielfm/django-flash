# -*- coding: utf-8 -*-

"""This package provides some built-in flash serialization codecs.
"""

import base64

from django.conf import settings
from django.utils.hashcompat import md5_constructor


class BaseCodec(object):
    """Base codec implementation. All codec implementations must extend this
    class.
    """
    def __init__(self):
        """Returns a new :class:`BaseCodec` object.
        """
        pass

    def encode(self, flash):
        """Empty implementation that raises :class:`NotImplementedError`.
        """
        raise NotImplementedError

    def decode(self, encoded_flash):
        """Empty implementation that raises :class:`NotImplementedError`.
        """
        raise NotImplementedError

    def encode_and_sign(self, flash):
        """Returns an encoded-and-signed version of the given *flash*.
        """
        encoded = self.encode(flash)
        encoded_md5 = md5_constructor(encoded + settings.SECRET_KEY).hexdigest()
        return base64.encodestring(encoded + encoded_md5)

    def decode_signed(self, encoded_flash):
        """Restores the *flash* object from the given encoded-and-signed data.
        """
        decoded_flash = base64.decodestring(encoded_flash)
        encoded, tamper_check = decoded_flash[:-32], decoded_flash[-32:]
        hex_digest = md5_constructor(encoded + settings.SECRET_KEY).hexdigest()
        if hex_digest != tamper_check:
            from django.core.exceptions import SuspiciousOperation
            raise SuspiciousOperation('User tampered with data.')
        try:
            return self.decode(encoded)
        except:
            # Errors might happen when decoding. Return None if that's the case
            return None


# Alias for use in settings file --> name of module in "codec" directory.
# Any codec that is not in this dictionary is treated as a Python import
# path to a custom codec.

# This config style is deprecated in Django 1.2, but we'll continue to support
# these alias for some more time.
CODECS = {
    'json': 'json_impl',
    'json_zlib': 'json_zlib_impl',
    'pickle': 'pickle_impl',
}

def get_codec(module):
    """Creates and returns the codec defined in the given module path
    (ex: ``"myapp.mypackage.mymodule"``). The argument can also be an alias to
    a built-in codec, such as ``"json"``, ``"json_zlib"`` or ``"pickle"``.
    """
    if module in CODECS:
        # The "_codec" suffix is to avoid conflicts with built-in module names
        mod = __import__('djangoflash.codec.%s' % CODECS[module], \
            {}, {}, [''])
    else:
        mod = __import__(module, {}, {}, [''])
    return getattr(mod, 'CodecClass')()

# Get the codec specified in the project's settings. Use the json codec by
# default, for security reasons: http://nadiana.com/python-pickle-insecure
codec = get_codec(getattr(settings, 'FLASH_CODEC', 'json'))
