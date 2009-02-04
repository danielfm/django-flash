# -*- coding: utf-8 -*-

"""
This module provides the context processors that exposes the
:class:`djangoflash.models.FlashScope` object to view's templates.

In order to plug Django-flash to your project, open your project's
``settings.py`` file and do the following changes::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'djangoflash.context_processors.flash',
    )


Doing this your view templates will be able to access the flash scope
contents using the ``flash`` context variable.
"""

def flash(request):
    """This context processor gets the :class:`djangoflash.models.FlashScope`
    object from the current *request* and adds it to the template context::
    
        <html>
            <head></head>
            <body>
                request.flash['message'] = {{ flash.message }}
            </body>
        </html>
    
    """
    return {'flash':request.flash}
