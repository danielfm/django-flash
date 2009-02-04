# -*- coding: utf-8 -*-

"""
This module provides the :class:`FlashMiddleware` class, which is
responsible manage the flash context when HTTP requests arrives.

In order to plug Django-flash to your project, open your project's
``settings.py`` file and do the following change::

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'djangoflash.middleware.FlashMiddleware',
    )


This is necessary because Django-flash relies on the user's session to store
the contents of the flash scope, you need to declare those two middleware
classes.

.. warning::

  The :class:`FlashMiddleware` class must be declared after the
  :class:`SessionMiddleware` class.
"""

from djangoflash.models import FlashScope


class FlashMiddleware(object):
    """This middleware is responsible to retrieve
    :class:`djangoflash.models.FlashScope` objects from the user's session
    or create them if necessary, as well as handle the expiration of old
    flash-scoped objects.
    """
    
    @staticmethod
    def get_context_from_request(request):
        """Gets the :class:`FlashScope` object from the request and returns
        it. If it couldn't be found, the method returns a brand new
        :class:`FlashScope` object.
        """
        context = FlashScope()
        if hasattr(request, 'flash'):
            context = request.flash
            if not isinstance(context, FlashScope):
                raise TypeError('Invalid Flash scope object: %s' % \
                    repr(context))
        return context
    
    @staticmethod
    def get_context_from_session(request):
        """Gets the :class:`FlashScope` object from the user's session and
        increments the age of flash-scoped objects. If this object couldn't
        be found, this method returns a brand new :class:`FlashScope` object.
        """ 
        context = FlashScope()
        if hasattr(request, 'session') and 'flash' in request.session:
            context = request.session['flash']
            context.increment_age()
        return context
    
    @staticmethod
    def process_request(request):
        """This method is called by the Django framework when a *request*
        arrives. You don't have to call it yourself.
        """
        request.flash = FlashMiddleware.get_context_from_session(request)
    
    @staticmethod
    def process_response(request, response):
        """This method is called by the Django framework when a *response* is
        sent back to the user.
        """
        if hasattr(request, 'session'):
            context = FlashMiddleware.get_context_from_request(request)
            if not context.is_current_empty():
                request.session['flash'] = context
        return response
