# -*- coding: utf-8 -*-

"""This middleware class searches for a request attribute called 'flash' in the
request object. If this attribute exists during the response phase, a session
attribute called 'flash' is registered in user's session.

To make this work, make sure to register this middleware after the
'django.contrib.sessions.middleware.SessionMiddleware' middleware in your
settings.py file.
"""

class _FlashScope(dict):
    """This class is just a dictionary with steroids, that also allows you to
    manipulate its values using dynamic attributes.
    """
    def __getattr__(self, key):
        "Get a value from the map."
        return self[key]
    
    def __setattr__(self, key, value):
        "Set a value on the map."
        self[key] = value


class FlashMiddleware(object):
    """
    This middleware class adds a Rails-like 'flash' scope, used to make it
    easier to apply the 'Redirect After Post' pattern.
    """
    
    def process_request(request):
        request.flash = _FlashScope()
    
    process_request = staticmethod(process_request)
    
    def process_response(request, response):
        """
        Add the flash message to the session, if it exists in the request
        object.
        """
        try:
            if request.flash:
                if not hasattr(request.flash, '__len__') or len(request.flash) == 0:
                    return response
                request.session['flash'] = request.flash
        except AttributeError:
            # It's okay... really
            pass
        
        return response
    
    process_response = staticmethod(process_response)
