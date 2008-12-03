# -*- coding: utf-8 -*-

"""This context processor is responsible to manage the 'flash' session attribute and
to expose its value to the view's context.
"""

from djangoflash.middleware import FLASH_KEY

FLASH_CONTEXT_VAR = 'flash'

def flash(request):
    """
    Add the variable 'flash' to the request context, if it exists.
    """
    if FLASH_KEY in request.session:
        return {FLASH_CONTEXT_VAR: request.session.pop(FLASH_KEY)}
    return {FLASH_CONTEXT_VAR: None}
