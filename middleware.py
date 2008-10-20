# -*- coding: utf-8 -*-

"""
This middleware class searches for a request attribute called 'flash' in the
request object. If this attribute exists during the response phase, a session
attribute called 'flash' is registered in user's session.

To make this work, make sure to register this middleware after the
'django.contrib.sessions.middleware.SessionMiddleware' middleware in your
settings.py file.
"""

class FlashMiddleware(object):
    """
    This middleware class adds a Rails-like 'flash' scope, used to make it
    easier to apply the 'Redirect After Post' pattern.
    """
    
    def process_response(request, response):
        """
        Add the flash message to the session, if it exists in the request
        object.
        """
        try:
            request.session['flash'] = request.flash
        except AttributeError:
            # It's okay... really
            pass
        
        return response
    
    process_response = staticmethod(process_response)
