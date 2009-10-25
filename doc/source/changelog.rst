.. _changelog:

Changelog
=========

Like any other piece of software, Django-Flash is evolving at each release.
Here you can track our progress:

**Version 1.7:**

* Added support for custom flash serialization codecs;
* Three built-in codec implementations: JSON, JSON/zlib and Pickle;
* Module :mod:`djangoflash.storage.base` removed;

**Version 1.6.3:**

* Using the ``DEBUG`` setting as the default value of ``FLASH_IGNORE_MEDIA``;

**Version 1.6.2:**

* Done some work to avoid the loss of messages when the
  :class:`CommonMiddleware` returns a :class:`HttpResponseRedirect` due to a
  missing trailing slash;

**Version 1.6.1:**

* Now the middleware checks if the request resolves to
  :meth:`django.views.static.serve` instead of relying on the ``MEDIA_URL``
  setting;

**Version 1.6:**

* Fixed a bug in which messages are prematurely removed from the flash when
  they are replaced using ``flash.now`` in some circumstances;
* Added the ``FLASH_IGNORE_MEDIA`` setting to let the user choose whether
  requests to static files should be ignored;

**Version 1.5.3:**

* Fixed a bug in the middleware which causes flash data to be dicarded after
  requests to static files;

**Version 1.5.2:**

* Added a :meth:`djangoflash.decorators.keep_messages` decorator for keeping
  flash messages;
* New ``AUTHORS`` file;

**Version 1.5.1:**

* Added a method :meth:`djangoflash.models.FlashScope.add` that simplifies the
  storage of multiple values under the same key;

**Version 1.5:**

* License changed from LGPL to BSD to give uses more freedom;
* Added support for custom flash storage backends;
* Added a cookie-based flash storage;
* Default session-based storage was factored out to an independent class;
* Added a few more sanity checks;

**Version 1.4.4:**

* Fixed a critical bug in the middleware;

**Version 1.4.3:**

* Added a few more sanity checks;

**Version 1.4.2:**

* Deprecating method :meth:`djangoflash.models.FlashScope.has_key`;
* Documentation improvements;
* Internals refactoring;

**Version 1.4.1:**

* Immediate values (:attr:`djangoflash.models.FlashScope.now`) can be
  manipulated using a dict-like syntax;
* Unit test improvements;
* Documentation improvements;

**Version 1.4:**

* **Notice:** *breaks backwards compatibility;*
* Now Django-Flash works pretty much like the original `Ruby on Rails`_' flash;
* Several code optmizations;
* Several improvements on the test suite;

**Version 1.3.5:**

* Several documentation improvements;
* Improvements on source code comments and unit tests;

**Version 1.3.4:**

* Added Sphinx_-based documentation;
* Source code changed to improve the Pylint_ score;
* :mod:`djangoflash` module now have a ``__version__`` property, which is
  very useful when you need to know what version of the Django-Flash is
  installed in your machine;

**Version 1.3.3:**

* *Critical Bug Fixed*: Django-Flash creates several useless session
  entries when the cookie support in user's browser is disabled;
* Small improvements on unit tests; 

**Version 1.3.2:**

* Small fixes;

**Version 1.3.1:**

* Added some sanity checks;

**Version 1.3:**

* **Notice:** *breaks backwards compatibility;*
* Django-Flash now controls the expiration of flash-scoped values
  individually, which means that only expired values are removed from the
  session (and not the whole flash context);
* Unit testing code was completely rewritten and now a real Django
  application is used in integration tests;
* Huge source code review to make it easier to read and to assure the use
  of Python conventions;
* Project renamed to **Django-Flash** (it was previously called
  **djangoflash**, without the hyphen);

**Version 1.2:**

* **Notice:** *breaks backwards compatibility;*
* Improvements on the test comments;
* Now the flash scope works pretty much like a :class:`dict`, although
  still there's no value-based expiration (the whole flash scope expires at
  the end of the request);

**Version 1.1:**

* Now using SetupTools_ to make the project easier to distribute;

**Version 1.0:**

* First (very simple) version;


.. _Ruby on Rails: http://www.rubyonrails.org/
.. _SetupTools: http://pypi.python.org/pypi/setuptools/
.. _Sphinx: http://sphinx.pocoo.org/
.. _Pylint: http://www.logilab.org/857
