Django-flash --- Rails-like *flash* messages support for Django
===============================================================

Django-flash is a simple Django extension that provides support for Rails_-like
*flash* messages.

The *flash* is a temporary storage mechanism -- kept in the user's session --
that looks like a Python dictionary, so you can store values associated with keys
and later retrieve them. It has one special property: by default, values stored
into the *flash* during the processing of a request will be available during the
processing of the immediately following request. Once that second request has
been processed, those values are removed automatically from the *flash*.

This is an open source project licenced under the terms of the
`Lesser General Public License v3.0`_ and sponsored by
`Destaquenet Technology Solutions`_, a brazilian software development and
consultancy startup.

  .. seealso::
     `PDF version <http://djangoflash.destaquenet.com/django-flash.pdf>`_ of
     this documentation.


Documentation contents
----------------------

.. toctree::
   :maxdepth: 3

   installation
   configuration
   usage
   modules/index
   getting_involved
   changelog


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Contact information
-------------------

  :Author: Daniel Fernandes Martins <daniel@destaquenet.com>
  :Company: `Destaquenet Technology Solutions`_


.. _Lesser General Public License v3.0: http://www.gnu.org/licenses/lgpl-3.0.html
.. _Django: http://www.djangoproject.org/
.. _Rails: http://www.rubyonrails.org/
.. _Destaquenet Technology Solutions: http://www.destaquenet.com/

