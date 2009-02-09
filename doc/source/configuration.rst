Configuration
-------------

In order to plug Django-flash to your project, open your project's
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

