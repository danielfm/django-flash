# -*- coding: utf-8 -*-

"""
This module provides the context processor that exposes
:class:`djangoflash.models.FlashScope` objects to view templates.

To plug this context processor to your Django project, edit your project's
``settings.py`` file as follows::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'djangoflash.context_processors.flash',
    )


Doing this, the view templates will be able to access the *flash* contents
using the ``flash`` context variable.

.. warning::
   Your views should use the :class:`RequestContext` class to render the
   templates, otherwise the ``flash`` variable (along with *all* other
   variables provided by other context processors) won't be available to them.
   Please read the
   `Django docs <http://docs.djangoproject.com/en/dev/ref/templates/api/>`_
   for further instructions.

"""

from django.core.exceptions import SuspiciousOperation
from djangoflash.models import FlashScope


# Name of the variable used to keep FlashScope objects both as an attribute
# django.http.HttpRequest and the template context.
CONTEXT_VAR = 'flash'

def flash(request):
    """This context processor gets the :class:`FlashScope` object from the
    current *request* and adds it to the template context:
    
    .. code-block:: html+django
    
       <html>
           <head></head>
           <body>
               request.flash['message'] = {{ flash.message }}
           </body>
       </html>
    
    """
    flash_scope = None
    try:
        flash_scope = getattr(request, CONTEXT_VAR)
        if not isinstance(flash_scope, FlashScope):
            raise SuspiciousOperation('Invalid flash: %s' % repr(flash_scope))
    except AttributeError:
        # Exposes empty flash when none is available
        flash_scope = FlashScope()
    return {CONTEXT_VAR: flash_scope}
