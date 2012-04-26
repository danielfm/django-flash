.. _configuration:

Configuration
-------------

In order to plug Django-Flash to your project, open your project's
``settings.py`` file and do the following changes::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'djangoflash.context_processors.flash',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'djangoflash.middleware.FlashMiddleware',
    )


That's all the required configuration.

.. warning::
  The :class:`djangoflash.middleware.FlashMiddleware` class must be declared
  after the :class:`SessionMiddleware` class.


Django-Flash and requests to media files
````````````````````````````````````````

Django itself doesn’t serve static (media) files, such as images, style sheets,
or video. It leaves that job to whichever web server you choose. But, *during
development*, you can use the :meth:`django.views.static.serve` view to serve
media files.

The problem with it is that, as a regular view, requests to
:meth:`django.views.static.serve` trigger the installed middlewares. And since
the *flash* gets updated by :ref:`a middleware <middleware>`, messages might be
removed from the *flash* by accident if the response causes the web browser to
issue requests to fetch static files.

To make Django-Flash work well with the :meth:`django.views.static.serve` view,
you can add the setting ``FLASH_IGNORE_MEDIA`` to your project's
``settings.py`` file::

    FLASH_IGNORE_MEDIA = True # Optional. Default: DEBUG

Set the ``FLASH_IGNORE_MEDIA`` setting to ``True``, and Django-Flash won't
remove any message from the *flash* if the request URL resolves to
:meth:`django.views.static.serve`.  Otherwise, every request will trigger the
:class:`djangoflash.middleware.FlashMiddleware` as usual.

.. note::
   This setting is optional; its default value is ``DEBUG``. So, if you adjust
   the ``DEBUG`` setting according to the environment in which the application
   runs (as you *should*), you don't have to worry about this setting at all,
   things will just work.


Flash storage backends
``````````````````````

Since :ref:`version 1.5<changelog>`, Django-Flash supports custom flash
storage backends.

By default, Django-Flash provides two built-in storage backends:

* :mod:`djangoflash.storage.session` -- Session-based storage (default);
* :mod:`djangoflash.storage.cookie` -- Cookie-based storage;

.. seealso::
   :ref:`custom_storages`


Using the session-based storage
'''''''''''''''''''''''''''''''

Django-Flash uses the :ref:`session-based storage <storage_session>` by default,
so you don't need to do anything else to use it.

*Although you are not required to do so*, you can add the following setting to
your project's ``settings.py`` file to make it clear about what flash storage
backend is being used::

    FLASH_STORAGE = 'session' # Optional


This storage backend *doesn't* rely on codecs to serialize and de-serialize the
flash data; it lets Django handle this.


Using the cookie-based storage
''''''''''''''''''''''''''''''

If you want to use the :ref:`cookie-based storage <storage_cookie>` instead the
default one, then add the following setting to the ``settings.py`` file::

    FLASH_STORAGE = 'cookie'


Since cookies will be used to store the contents of the flash scope,
Django-Flash doesn't require you to add the :class:`SessionMiddleware` class
to the ``MIDDLEWARE_CLASSES`` section of your project's settings anymore.

This storage backend relies on codecs to serialize and de-serialize the flash
data.


Flash serialization codecs
``````````````````````````

Since :ref:`version 1.7<changelog>`, Django-Flash supports custom flash
serialization codecs.

By default, Django-Flash provides three built-in codecs:

* :mod:`djangoflash.codec.json_impl` -- JSON-based codec (default);
* :mod:`djangoflash.codec.json_zlib_impl` -- JSON/zlib-based codec;
* :mod:`djangoflash.codec.pickle_impl` -- Pickle-based codec;

.. seealso::
   :ref:`custom_codecs`


Using the JSON-based codec implementation
'''''''''''''''''''''''''''''''''''''''''

For security reasons, Django-flash uses the 
:ref:`JSON-based codec implementation <json_codec>` by default, so you don't
need to do anything else to use it.

*Although you are not required to do so*, you can add the following setting to
your project's ``settings.py`` file to make it clear about what codec
implementation is being used::

    FLASH_CODEC = 'json' # Optional


There's also an :ref:`alternative version <json_zlib_codec>` of this codec that
uses the :mod:`zlib` module to reduce the encoded flash footprint. This is
particularly useful when the flash storage backend in use (such as the 
:ref:`cookie-based storage <storage_cookie>`) cannot handle the amount of data
in the *flash*::

    FLASH_CODEC = 'json_zlib'


Using the Pickle-based codec implementation
'''''''''''''''''''''''''''''''''''''''''''

If you want to use the :ref:`Pickle-based codec implementation <pickle_codec>`
instead the default one, then add the following setting to the ``settings.py``
file::

    FLASH_CODEC = 'pickle'


.. warning::
   The use of this codec is not recommended since the
   `Pickle documentation <http://docs.python.org/library/pickle.html>`_ itself
   clearly states that it's not intended to be secure against erroneous or
   maliciously constructed data.

