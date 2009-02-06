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

.. warning::

   Your views should use the :class:`RequestContext` class to render the view
   templates, otherwise the ``flash`` variable (along with *all* other
   variables provided by other context processors) won't be available to you.
   Please read the
   `Django documentation <http://docs.djangoproject.com/en/dev/ref/templates/api/>`_
   for further instructions.

"""

CONTEXT_VAR = 'flash'

def flash(request):
    """This context processor gets the :class:`FlashScope` object from the
    current *request* and adds it to the template context::
    
        <html>
            <head></head>
            <body>
                request.flash['message'] = {{ flash.message }}
            </body>
        </html>
    
    """
    return {CONTEXT_VAR:request.flash}
