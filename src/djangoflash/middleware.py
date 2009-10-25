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
from django.core import urlresolvers
from django.views.static import serve

from djangoflash.context_processors import CONTEXT_VAR
from djangoflash.models import FlashScope
from djangoflash.storage import storage


# This middleware integrates gracefully with CommonMiddleware
_COMMON_MIDDLEWARE_CLASS = 'django.middleware.common.CommonMiddleware'


class FlashMiddleware(object):
    """This middleware uses the flash storage backend specified by the
    project's ``settings.py`` file in order to store and retrieve
    :class:`djangoflash.models.FlashScope` objects, being also responsible for
    expiring old flash-scoped objects.

    .. note::
       This class is designed to be used by the Django framework itself.
    """

    def process_request(self, request):
        """This method is called by the Django framework when a *request* hits
        the server.
        """
        flash = _get_flash_from_storage(request)
        if _should_update_flash(request):
            flash.update()

    def process_response(self, request, response):
        """This method is called by the Django framework when a *response* is
        sent back to the user.
        """
        flash = _get_flash_from_request(request)
        if flash:
            storage.set(flash, request, response)
        else:
            _get_flash_from_storage(request)

        return response


def _get_flash_from_storage(request):
    """Gets the flash from the storage, adds it to the given request and
    returns it. A new :class:`FlashScope` is used if the storage is empty.
    """
    flash = storage.get(request) or FlashScope()
    setattr(request, CONTEXT_VAR, flash)
    return flash

def _get_flash_from_request(request):
    """Returns the :class:`FlashScope` object from the given request. If it
    couldn't be found, returns None.
    """
    flash = None
    if hasattr(request, CONTEXT_VAR):
        flash = getattr(request, CONTEXT_VAR)
        if not isinstance(flash, FlashScope):
            raise SuspiciousOperation('Invalid flash: %s' % repr(flash))
    return flash

def _should_update_flash(request):
    """Returns True if the flash should be updated, False otherwise.
    """
    return not _is_trailing_slash_missing(request) and \
        not _is_request_to_serve(request)

def _is_request_to_serve(request):
    """Returns True if *request* resolves to the built-in ``serve`` view,
    False othersise.
    """
    # Are we running in debug mode?
    debug = getattr(settings, 'DEBUG', False)

    # Uses the value of DEBUG as default value to FLASH_IGNORE_MEDIA
    if getattr(settings, 'FLASH_IGNORE_MEDIA', debug):
        try:
            return urlresolvers.resolve(request.path_info)[0] == serve
        except urlresolvers.Resolver404:
            pass
    return False

def _is_trailing_slash_missing(request):
    """Returns True if the requested URL are elegible to be intercepted by the
    CommonMiddleware (if it's being used), which  issues a HttpRedirect when a
    trailing slash is missing. Returns False otherwise.
    """
    if _COMMON_MIDDLEWARE_CLASS in settings.MIDDLEWARE_CLASSES:
        path = request.path
        if getattr(settings, 'APPEND_SLASH', False) and not path.endswith('/'):
            if not _is_valid_path(path) and _is_valid_path('%s/' % path):
                return True
    return False

def _is_valid_path(path):
    """Returns True if *path* resolves against the default URL resolver,
    False otherwise.
    """
    try:
        urlresolvers.resolve(path)
        return True
    except urlresolvers.Resolver404:
        pass
    return False
