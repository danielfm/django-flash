# -*- coding: utf-8 -*-

"""
This module provides the :class:`FlashMiddleware` class, which manages the
*flash* whenever a HTTP request hits the server.

To plug this middleware to your Django project, edit your project's
``settings.py`` file as follows::

    MIDDLEWARE_CLASSES = (
        'djangoflash.middleware.FlashMiddleware',
    )
"""

from urlparse import urlparse

from django.conf import settings
from django.core.exceptions import SuspiciousOperation

from djangoflash.context_processors import CONTEXT_VAR
from djangoflash.models import FlashScope
from djangoflash.storage import storage


class FlashMiddleware(object):
    """This middleware uses the flash storage backend specified by the
    project's ``settings.py`` file in order to store and retrieve
    :class:`djangoflash.models.FlashScope` objects, being also responsible for
    expiring old flash-scoped objects.

    .. note::
       This class is designed to be used by the Django framework itself.
    """

    def __init__(self):
        """Initialize this middleware.
        """
        pass

    def _get_flash_from_request(self, request):
        """Returns the :class:`FlashScope` object from the given request. If it
        couldn't be found, returns None.
        """
        flash = None
        if hasattr(request, CONTEXT_VAR):
            flash = getattr(request, CONTEXT_VAR)
            if not isinstance(flash, FlashScope):
                raise SuspiciousOperation('Invalid flash: %s' % repr(flash))
        return flash

    def _is_request_to_static_content(self, request):
        """Returns whether the given request points to a static resource.
        """
        media_path = urlparse(settings.MEDIA_URL)[2]
        request_path = urlparse(request.path_info)[2]
        return request_path.startswith(media_path)

    def process_request(self, request):
        """This method is called by the Django framework when a *request* hits
        the server.
        """
        flash = storage.get(request) or FlashScope()
        setattr(request, CONTEXT_VAR, flash)
        if not self._is_request_to_static_content(request):
            flash.update()

    def process_response(self, request, response):
        """This method is called by the Django framework when a *response* is
        sent back to the user.
        """
        storage.set(self._get_flash_from_request(request), request, response)
        return response
