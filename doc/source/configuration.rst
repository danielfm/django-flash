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


Flash storage backends
``````````````````````

Since :ref:`version 1.5<changelog>`, Django-Flash supports custom flash
storage backends.

By default, Django-Flash provides two built-in storage backends:

* :mod:`djangoflash.storage.session` -- Session-based storage (default);
* :mod:`djangoflash.storage.cookie` -- Cookie-based storage;


Using the session-based storage
'''''''''''''''''''''''''''''''

Django-Flash uses the :ref:`session-based storage <storage_session>` by default,
so you don't need to do anything else to use it.

*Although you are not required to do so*, you can add the following setting to
your project's ``settings.py`` file to make it clear about what flash storage
backend is being used::

    FLASH_STORAGE = 'session'


Using the cookie-based storage
''''''''''''''''''''''''''''''

If you want to use the :ref:`cookie-based storage <storage_cookie>` instead the
default one, then add the following setting to the ``settings.py`` file::

    FLASH_STORAGE = 'cookie'

Since cookies will be used to store the contents of the flash scope,
Django-Flash doesn't require you to add the :class:`SessionMiddleware` class
to the ``MIDDLEWARE_CLASSES`` section of your project's settings anymore.


Using a third-party storage
'''''''''''''''''''''''''''

To use a third-party flash storage backend, just set the module path to the
``FLASH_STORAGE`` setting in your project's ``settings.py`` file::

    FLASH_STORAGE = 'custom.storage.module.here'

.. seealso::
   :ref:`custom_storages`
