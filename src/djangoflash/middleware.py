# -*- coding: utf-8 -*-

"""This middleware uses the FlashScope class to manage the flash context.
The FlashMiddleware class runs on both request and response.

To plug it to your Django project, modify your project's settings.py like
this:

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'djangoflash.middleware.FlashMiddleware',
)

Make sure to put the FlashMiddleware *after* the SessionMiddleware.
"""

from djangoflash.models import FlashScope


class FlashMiddleware(object):
    """This middleware class adds a Rails-like 'flash' scope to the
    request object.
    """
    
    def get_context_from_request(self, request):
        """Gets the FlashScope object from the request and returns it. If this
        object couldn't be found, the method returns a brand new FlashScope
        object.
        """
        context = FlashScope()
        if hasattr(request, 'flash'):
            context = request.flash
            if not isinstance(context, FlashScope):
                raise TypeError('Invalid Flash scope object: %s' % \
                    repr(context))
        return context
    
    def get_context_from_session(self, request):
        """Gets the FlashScope object from the session and increments the
        age of flash-scoped objects. If this object couldn't be found, the
        method returns a brand new FlashScope object.
        """ 
        context = FlashScope()
        if hasattr(request, 'session') and 'flash' in request.session:
            context = request.session['flash']
            context.increment_age()
        return context
    
    def process_request(self, request):
        "Called by Django when a request arrives."
        request.flash = self.get_context_from_session(request)
    
    def process_response(self, request, response):
        "Called by Django when a response is sent."
        if hasattr(request, 'session'):
            context = self.get_context_from_request(request)
            if not context.is_current_empty():
                request.session['flash'] = context
        return response
