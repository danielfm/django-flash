# -*- coding: utf-8 -*-

"""This module provides decorators to simplify common tasks.
"""

from djangoflash.context_processors import CONTEXT_VAR


def keep_messages(*keys):
    """Prevents specific values from being removed during the processing of
    the decorated view. If this decorator is used with no args, the entire
    flash is preserved.
    """
    def _keep_messages(view_method):
        def _wrapped_view_method(request, *args, **kwargs):
            if hasattr(request, CONTEXT_VAR):
                flash = getattr(request, CONTEXT_VAR)
                flash.keep(*keys)
                return view_method(request, *args, **kwargs)
        return _wrapped_view_method

    if len(keys) == 1 and callable(keys[0]):
        view_method = keys[0]
        keys = []
        return _keep_messages(view_method)
    return _keep_messages
