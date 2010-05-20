# -*- coding: utf-8 -*-

"""This package provides some built-in flash storage backends used to persist
the *flash* contents across requests.
"""

from django.conf import settings


# Alias for use in settings file --> name of module in "storage" directory.
# Any storage that is not in this dictionary is treated as a Python import
# path to a custom storage.

# This config style is deprecated in Django 1.2, but we'll continue to support
# these alias for some more time.
STORAGES = {
    'session': 'session',
    'cookie': 'cookie',
}

def get_storage(module):
    """Creates and returns the flash storage backend defined in the given
    module path (ex: ``"myapp.mypackage.mymodule"``). The argument can also
    be an alias to a built-in storage backend, such as ``"session"`` or
    ``"cookie"``.
    """
    if module in STORAGES:
        mod = __import__('djangoflash.storage.%s' % STORAGES[module], \
            {}, {}, [''])
    else:
        mod = __import__(module, {}, {}, [''])
    return getattr(mod, 'FlashStorageClass')()

# Get the flash storage specified in the project's settings. Use the session
# storage by default (for both security and backward compatibility reasons).
storage = get_storage(getattr(settings, 'FLASH_STORAGE', 'session'))
