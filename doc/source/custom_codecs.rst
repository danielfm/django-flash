.. _custom_codecs:

Creating a custom serialization codec
-------------------------------------

Since :ref:`version 1.7 <changelog>`, Django-Flash supports custom flash
serialization codecs.

By default, Django-Flash provides three built-in codecs:

* :mod:`djangoflash.codec.json_impl` -- JSON-based codec (default);
* :mod:`djangoflash.codec.json_zlib_impl` -- JSON/zlib-based codec;
* :mod:`djangoflash.codec.pickle_impl` -- Pickle-based codec;

The good news is that you can create your own codec if the existing ones are
getting in your way. To do so, the first thing you need to do is create a
Python module with a class called :class:`CodecClass`::

    # Let's suppose this module is called 'myproj.djangoflash.custom'
    
    from djangoflash.codec import BaseCodec
    
    class CodecClass(BaseCodec):
        def __init__(self):
            BaseCodec.__init__(self)

        def encode(self, flash):
            pass

        def decode(self, encoded_flash):
            pass


Note that custom codecs must extend the :class:`djangoflash.codec.BaseCodec`
class direct or indirectly.

Finally, to use your custom codec, add the following setting to your project's
``settings.py`` file::

    FLASH_CODEC = 'myproj.djangoflash.custom' # Path to module


.. seealso::
   :ref:`configuration`

