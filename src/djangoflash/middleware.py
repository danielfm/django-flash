# -*- coding: utf-8 -*-

"""
This module provides the :class:`FlashMiddleware` class, which manages the
flash context whenever a HTTP requests hits the server.

To plug this middleware to your Django project, add the following snippet to
the ``settings.py`` file::

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'djangoflash.middleware.FlashMiddleware',
    )


You need to add the :class:`SessionMiddleware` because Django-flash relies on
user's session to store the contents of the flash scope.

.. warning::
   The :class:`FlashMiddleware` class must be declared after the
   :class:`SessionMiddleware` class.
"""

from djangoflash.models import FlashScope
from djangoflash.context_processors import CONTEXT_VAR


"""This value is used to identify the flash scope object inside the user's
session.
"""
_SESSION_KEY = '_djflash_app'


class FlashMiddleware(object):
    """This middleware puts/gets a :class:`djangoflash.models.FlashScope`
    object to/from the user's session, and triggers the expiration of old
    flash-scoped objects.
    
    .. note::
       This class is designed to be used by the Django framework itself.
    """
    
    @staticmethod
    def get_context_from_request(request):
        """Gets the :class:`FlashScope` object from the *request* and returns
        it. If it couldn't be found, the method returns a brand new
        :class:`FlashScope` object.
        """
        context = FlashScope()
        if hasattr(request, CONTEXT_VAR):
            context = getattr(request, CONTEXT_VAR)
            if not isinstance(context, FlashScope):
                raise TypeError('Invalid Flash scope object: %s' % \
                    repr(context))
        return context
    
    @staticmethod
    def get_context_from_session(request):
        """Gets the :class:`FlashScope` object from the user's session and
        :meth:`update` it. If this object couldn't be found, this method
        returns a brand new :class:`FlashScope` object.
        """ 
        context = FlashScope()
        if hasattr(request, 'session') and _SESSION_KEY in request.session:
            context = request.session[_SESSION_KEY]
            context.update()
        return context
    
    @staticmethod
    def process_request(request):
        """This method is called by the Django framework when a *request*
        hits the server.
        """
        setattr(request, CONTEXT_VAR, \
            FlashMiddleware.get_context_from_session(request))
    
    @staticmethod
    def process_response(request, response):
        """This method is called by the Django framework when a *response* is
        sent back to the user.
        """
        if hasattr(request, 'session'):
            context = FlashMiddleware.get_context_from_request(request)
            if len(context) > 0:
                request.session[_SESSION_KEY] = context
            elif _SESSION_KEY in request.session:
                del request.session[_SESSION_KEY]
        return response
