:mod:`djangoflash.models` --- Django-flash model
================================================

.. module:: djangoflash.models
   :synopsis: Django-flash model
.. moduleauthor:: Daniel Fernandes Martins <daniel@destaquenet.com>


The :mod:`djangoflash.models` module provides the :class:`FlashScope` class,
which is the one responsible to maintain the flash-scoped objects and control
their lifecycle.


Available Types
---------------


.. class:: FlashScope

   This is a dict-like object responsible to store the flash-scoped objects
   and control their lifecycle.

Subclass relationships::

   object
       FlashScope
