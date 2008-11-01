# -*- coding: utf-8 -*-

"""This context processor is responsible to manage the 'flash' session attribute and
to expose its value to the view's context.
"""

def flash(request):
    """
    Add the variable 'flash' to the request context, if it exists.
    """
    if 'flash' in request.session:
        message = request.session['flash']
        del request.session['flash']
        
        return {'flash': message}
    return {'flash': None}
