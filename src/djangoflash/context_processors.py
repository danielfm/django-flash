# -*- coding: utf-8 -*-

"""This context processor exposes the FlashScope object to view's templates.
The FlashScope object is the one who properly manages the flash context.

To install it to your Django project, modify your project's settings.py
like this:

TEMPLATE_CONTEXT_PROCESSORS = (
    ...
    'djangoflash.context_processors.flash',
    ...
)
"""

def flash(request):
    "Exposes the FlashScope object under the 'flash' context variable."
    return {'flash':request.flash}
