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


The first thing we did was to declare a template processor that exposes
the flash scope contents to your view templates. And, since Django-flash
relies on the user's session to store the contents of the flash scope, you
need to declare those two middleware classes.

That's all the required configuration.

.. warning::
  The :class:`FlashMiddleware` class must be declared after the
  :class:`SessionMiddleware` class.

