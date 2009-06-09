# -*- coding: utf-8 -*-

"""
This module provides the :class:`FlashMiddleware` class, which manages the
flash context whenever a HTTP request hits the server.

To plug this middleware to your Django project, edit your project's
``settings.py`` file as follows::

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


class FlashMiddleware(object):
    """This middleware puts/gets a :class:`djangoflash.models.FlashScope`
    object to/from the user's session, and triggers the expiration of old
    flash-scoped objects.

    .. note::
       This class is designed to be used by the Django framework itself.
    """

    """This value is used to identify the flash scope object inside the user's
    session.
    """
    _SESSION_KEY = '_djflash_app'

    def _get_context_from_request(self, request):
        """Gets the :class:`FlashScope` object from the *request* and returns
        it. If it couldn't be found, the method returns a brand new
        :class:`FlashScope` object.
        """
        context = None
        if hasattr(request, CONTEXT_VAR):
            context = getattr(request, CONTEXT_VAR)
            if not isinstance(context, FlashScope):
                raise TypeError('Invalid Flash scope object: %s' % \
                    repr(context))
        return context or FlashScope()

    def _get_context_from_session(self, request):
        """Gets the :class:`FlashScope` object from the user's session and
        :meth:`update` it. If this object couldn't be found, this method
        returns a brand new :class:`FlashScope` object.
        """ 
        context = None
        if FlashMiddleware._SESSION_KEY in request.session:
            context = request.session[FlashMiddleware._SESSION_KEY]
            context.update()
        return context or FlashScope()

    def process_request(self, request):
        """This method is called by the Django framework when a *request*
        hits the server.
        """
        assert hasattr(request, 'session'), """Django-flash middleware requires
session middleware to be  installed. Edit your MIDDLEWARE_CLASSES setting to
insert  'django.contrib.sessions.middleware.SessionMiddleware'."""
        setattr(request, CONTEXT_VAR, self._get_context_from_session(request))

    def process_response(self, request, response):
        """This method is called by the Django framework when a *response* is
        sent back to the user.
        """
        context = self._get_context_from_request(request)

        # The session attribute might not be set if CommonMiddleware steps in
        if hasattr(request, 'session'):
            if context:
                request.session[FlashMiddleware._SESSION_KEY] = context
            elif FlashMiddleware._SESSION_KEY in request.session:
                del request.session[FlashMiddleware._SESSION_KEY]
        return response
