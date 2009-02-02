.. django-flash documentation master file, created by sphinx-quickstart on Sun Feb  1 01:49:12 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django-flash --- Rails-like flash scope support for Django
==============================================================

Django-flash is a simple extension to the Django_ framework which enables the
use of the so called flash scope, first introduced by `Ruby on Rails`_ a
few years ago.

This is an open source project licenced under the terms of the
`Lesser General Public License v3.0`_ and sponsored by
`Destaquenet Technology Solutions`_, a brazilian software development and
consultancy startup.


Installation
------------

The easiest way to install Django-flash is via EasyInstall_. Follow
`these <http://pypi.python.org/pypi/setuptools>`_ instructions to install
EasyInstall if you don't have it already.

Then, execute the following command line to download and install the latest
stable version from CheeseShop_::

    $ easy_install django-flash

If you use git_ and want to get the latest *development* version from the
project website, at Github_::

    $ git clone git://github.com/danielfm/django-flash.git
    $ cd django-flash
    $ python setup.py install

Or get the latest *development* version as a tarball::

    $ wget http://github.com/danielfm/django-flash/tarball/master
    $ tar zxf danielfm-django-flash-XXXXXXXXXXXXXXXX.tar.gz
    $ cd danielfm-django-flash-XXXXXXXXXXXXXXXX
    $ python setup.py install


Configuration
-------------

In order to plug Django-flash to your Django_ project, open your project's
``settings.py`` file and do the following changes::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'djangoflash.context_processors.flash',
    )

    MIDDLEWARE_CLASSES = (
        # django-flash depends on the SessionMiddleware
        'django.contrib.sessions.middleware.SessionMiddleware',
        
        'djangoflash.middleware.FlashMiddleware',
    )

That's all the required configuration.


Using Django-flash
----------------------

Once plugged to your project, Django-flash automatically adds a ``flash``
attribute to the :class:`django.http.HttpRequest` objects received by your view
methods. This property points to an instance of
:class:`FlashScope`.

Here goes some examples on how to manipulate this scope::

    def my_view(request):
        # Puts a string to the flash scope
        request.flash['key'] = 'value'
        
        # Same as above
        request.flash.put(key='value')
        
        # Checks if the object is available at the flash scope
        'key' in request.flash
        
        # Gets an object from the flash scope
        request.flash['key']
        
        # Same as above, but returns a default value if the key doesn't exists
        request.flash.get('key', 'default value')
        
        # Removes an object from the flash scope
        del request.flash['key']


Although we are using plain strings values, you are free to use any
*pickleable* object.


Flash-scoped objects: default lifecycle
```````````````````````````````````````

First let's see a basic example of how Django-flash controls the
flash-scoped objects lifecycle. Consider the following view methods::

    # URL: http://server/app/first
    def first_view(request):
        request.flash['message'] = 'My message'
        print 'message' in request.flash # output: False
        return HttpResponseRedirect(reverse(second_view))
    
    # URL: http://server/app/second
    def second_view(request):
        print request.flash['message'] # Output: My message
        request.flash['another_message'] = 'Something'
        print 'another_message' in request.flash # output: False
        return HttpResponseRedirect(reverse(third_view))
    
    # URL: http://server/app/third
    def third_view(request):
        print request.flash['another_message'] # Output: Something
        print 'message' in request.flash # output: False
        return HttpResponseRedirect(reverse(fourth_view))
    
    # URL: http://server/app/fourth
    def fourth_view(request):
        return HttpResponse(...)


Let's say that we have opened our web browser and issued a request to
http://server/app/first\. When the ``first_view`` method executes, it first
sets a flash-scoped object under the ``message`` key. Since this object will
*only become available on the next request*, the next line of code prints
``False``. The last line returns a HTTP Redirect, which causes our browser to
issue a ``GET`` request to http://server/app/second\.

When the ``second_view`` method executes, it first prints the content of the
flash-scoped object under the ``message`` key, which is now available. The
next line of code sets another flash-scoped object under the
``another_message`` key. Just like happened before, this object will only
become available on the next request. Again, the last line returns a HTTP
Redirect, which causes our browser to issue a ``GET`` request to
http://server/app/third\.

When the ``third_view`` method executes, the flash-scoped object under the
``another_message`` key is now available, which is not a surprise. But, at
the same time, the flash-scoped object added by ``first_view`` was
automatically removed from the flash scope.


Lifecycle management
````````````````````

By default, values stored into the flash scope during the processing of a
request will be available during the processing of the immediately following
request. Once that second request has been processed, those values are
automatically removed.

As we'll see below, this default behavior might not be enough in some
situations though.


Preventing flash-scoped objects from being removed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can prevent a flash-scoped object from being removed by using the
``keep`` method::

    def first_view(request):
        request.flash['message'] = 'Operation succeeded!'
        return HttpRedirectResponse(reverse(second_view))
        
    def second_view(request):
        print request.flash['message'] # Output: Operation succeeded!
        request.flash.keep('message')
        return HttpRedirectResponse(reverse(third_view))
    
    def third_view(request):
        print request.flash['message'] # Output: Operation succeeded!
        return HttpRedirectResponse(reverse(fourth_view))
    
    def fourth_view(request):
        print 'message' in request.flash # Output: False
        return HttpResponse(...)


You can also keep *all* active flash-scoped objects by calling the
``keep`` method with no arguments::

    def second_view(request):
        request.flash.keep()
        return HttpRedirectResponse(reverse(third_view))


Adding an immediate flash-scoped object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It's sometimes convenient to add an object to the flash scope and use it
on the current request. This can be done by using the ``now`` method::

    def first_view(request):
        request.flash.now(message='My message')
        print request.flash['message'] # Output: My message


**Note:** Objects added to the flash scope using the ``now`` method are
*transient*, which means you cannot ``keep`` them around for the
next request::

    def first_view(request):
        request.flash.now(message='My message')
        print request.flash['message'] # Output: My message
        request.flash.keep()
        return HttpRedirectResponse(reverse(second_view))
    
    def second_view(request):
        print 'message' in request.flash # Output: False
        return HttpResponse(...)


Accessing flash-scoped objects from view templates
``````````````````````````````````````````````````

We already know how to access the flash scope from a view method. But what
about the view templates? ::

    <html>
    <head>
        <title>My template</title>
    </head>
    <body>
        {% if flash.message %}
            <!-- There's a flash-scoped object under the 'message' key -->
            
            <div class="flash_message">
                <p>{{ flash.message }}</p>
            </div>
        {% endif %}
    </body>
    </html>


It's also possible to iterate over all active flash-scoped objects using the
``{% for %}`` tag if you want to::

    <html>
    <head>
        <title>My template</title>
    </head>
    <body>
        {% if flash %}
            <!-- There's one or more flash-scoped objects -->
            
            {% for value in flash.values %}
                <div class="flash_entry">
                    <p>{{ value }}</p>
                </div>
            {% endfor %}
        {% endif %}
    </body>
    </html>


Credits
-------

  :Author: Daniel Fernandes Martins <daniel@destaquenet.com>
  :Company: `Destaquenet Technology Solutions`_


Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Lesser General Public License v3.0: http://www.gnu.org/licenses/lgpl-3.0.html

.. _Django: http://www.djangoproject.org/
.. _Ruby on Rails: http://www.rubyonrails.org/
.. _Destaquenet Technology Solutions: http://www.destaquenet.com/
.. _EasyInstall: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _CheeseShop: http://pypi.python.org/pypi
.. _Github: http://github.com/danielfm/django-flash/tree/master
.. _git: http://git-scm.com/

