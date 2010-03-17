Django-Flash
============

Django-Flash is a simple Django extension that provides support for Rails_-like
*flash* messages.

The *flash* is a temporary storage mechanism that looks like a Python
dictionary, so you can store values associated with keys and later retrieve
them. It has one special property: by default, values stored into the *flash*
during the processing of a request will be available during the processing of
the immediately following request. Once that second request has been
processed, those values are removed automatically from the storage.

This is an open source project licenced under the terms of The
`BSD License`_ and sponsored by `Destaquenet Technology Solutions`_, a
brazilian software development and consultancy startup.


Installation and Usage
----------------------

Please read the `online documentation <http://djangoflash.destaquenet.com/>`_
for further instructions.


.. _BSD License: http://www.opensource.org/licenses/bsd-license.php
.. _Django: http://www.djangoproject.org/
.. _Rails: http://www.rubyonrails.org/
.. _Destaquenet Technology Solutions: http://www.destaquenet.com/
