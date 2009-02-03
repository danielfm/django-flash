# -*- coding: utf-8 -*-

"""This module provides the context processors that exposes the
:class:`djangoflash.models.FlashScope` object to view's templates.

To install it to your Django project, modify your project's ``settings.py``
like this::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'djangoflash.context_processors.flash',
        ...
    )
"""

def flash(request):
    """This context processor gets the :class:`djangoflash.models.FlashScope`
    object from the current :class:`HttpRequest` and adds it to the template
    context::
    
        <html>
            <head></head>
            <body>
                request.flash['message'] = {{ flash.message }}
            </body>
        </html>
    
    """
    return {'flash':request.flash}
