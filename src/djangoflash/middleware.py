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
from django.core.urlresolvers import resolve
from django.http import Http404
from django.views.static import serve

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

    def _should_update_flash(self, request):
        """Returns whether the flash should be updated.
        """
        if getattr(settings, 'FLASH_IGNORE_MEDIA', False):
            try:
                return resolve(request.path_info)[0] != serve
            except Http404:
                pass
        return True

    def process_request(self, request):
        """This method is called by the Django framework when a *request* hits
        the server.
        """
        flash = storage.get(request) or FlashScope()
        setattr(request, CONTEXT_VAR, flash)
        if self._should_update_flash(request):
            flash.update()

    def process_response(self, request, response):
        """This method is called by the Django framework when a *response* is
        sent back to the user.
        """
        storage.set(self._get_flash_from_request(request), request, response)
        return response
