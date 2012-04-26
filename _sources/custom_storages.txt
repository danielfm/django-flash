.. _custom_storages:

Creating a custom flash storage backend
---------------------------------------

Since :ref:`version 1.5<changelog>`, Django-Flash supports custom flash
storage backends.

By default, Django-flash provides two built-in storage backends:

* :mod:`djangoflash.storage.session` -- Session-based storage (default);
* :mod:`djangoflash.storage.cookie` -- Cookie-based storage;

The good news is that you can create your own storage backend if the existing
ones are getting in your way. To do so, the first thing you need to do is
create a Python module with a class called :class:`FlashStorageClass`::

    # Let's suppose this module is called 'myproj.djangoflash.custom'

    # You can use the serialization codec configured by the user
    from djangoflash.codec import codec
    
    class FlashStorageClass(object):
        def _is_flash_stored(self, request):
            # This method checks whether the flash is already stored
            pass
        
        def set(self, flash, request, response):
            if flash:
                # Store the flash
                pass
            elif self._is_flash_stored(request):
                # Flash is null or empty, so remove the already stored flash
                pass

        def get(self, request):
            if self._is_flash_stored(request):
                # Return the stored flash
                pass


Then, to use your custom flash storage backend, add the following setting
to your project's ``settings.py`` file::

    FLASH_STORAGE = 'myproj.djangoflash.custom' # Path to module


.. seealso::
   :ref:`configuration`

