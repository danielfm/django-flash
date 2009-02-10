Using Django-flash
------------------

Once plugged to your project, Django-flash automatically adds a ``flash``
attribute to the :class:`django.http.HttpRequest` objects received by your
views. This property points to a :class:`djangoflash.models.FlashScope`
instance.

Here goes some examples on how to manipulate this scope from a view::

    def my_view(request):
        # Puts a string to the flash scope
        request.flash['key'] = 'value'
        
        # Alternative syntax that does the same as above
        request.flash.put(key='value')
        
        # Checks if the object is available at the flash scope
        'key' in request.flash
        
        # Gets an object from the flash scope
        request.flash['key']
        
        # Removes an object from the flash scope
        del request.flash['key']


Although we are using just *string* values, you are free to use any *pickleable*
object.

To see the list of all methods available to you, take a look at the
:class:`djangoflash.models.FlashScope` documentation.


.. _flash-default-lifecycle:

Flash-scoped objects: the default lifecycle
```````````````````````````````````````````

First let's see a basic example of how Django-flash controls the
flash-scoped objects lifecycle. Consider the following views::

    # URL: http://server/app/first
    def first_view(request):
        request.flash['message'] = 'My message'
        return HttpResponseRedirect(reverse(second_view))
    
    # URL: http://server/app/second
    def second_view(request):
        print request.flash['message'] # Output: My message
        request.flash['another_message'] = 'Something'
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
http://server/app/first\. When the :meth:`first_view` method executes, it
first sets a flash-scoped object under the ``message`` key. The last line
returns a HTTP Redirect, which causes our browser to issue a ``GET`` request
to http://server/app/second\.

When the :meth:`second_view` method executes, it first prints the content of
the flash-scoped object under the ``message`` key, which is still available.
The next line of code sets another flash-scoped object under the
``another_message`` key. Again, the last line returns a HTTP Redirect, which
causes our browser to issue a ``GET`` request to http://server/app/third\.

When the :meth:`third_view` method executes, the flash-scoped object under
the ``another_message`` key is now available, which is not a surprise. But,
at the same time, the flash-scoped object added by :meth:`first_view` was
automatically removed.


.. seealso::
   :ref:`modulesindex`


Lifecycle management
````````````````````

By default, all objects stored inside the flash context survives until the
*very next* request, being automatically removed after that. Unfortunately,
this default behavior might not be enough in some situations.


Preventing flash-scoped objects from being removed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can prevent flash-scoped objects from being removed by using the
:meth:`FlashScope.keep` method::

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


If you want to keep *all* flash-scoped objects, just call the :meth:`keep`
method with no arguments::

    def second_view(request):
        request.flash.keep()
        return HttpRedirectResponse(reverse(third_view))


Adding an immediate flash-scoped object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It's sometimes convenient to add an object to the flash scope and use it
on the *current* request only.

This can be done by using the :attr:`FlashScope.now` attribute::

    def first_view(request):
        request.flash.now['message'] = 'My message'
        request.flash.now(message='My message') # Alternative syntax
        print request.flash['message'] # Output: My message
        return HttpRedirectResponse(reverse(second_view))
    
    def second_view(request):
        print 'message' in request.flash # Output: False


Accessing flash-scoped objects from view templates
``````````````````````````````````````````````````

We already know how to access the flash scope from a views. But what about
the view templates?

Well, it's just as easy:

.. code-block:: html+django

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


It's also possible to iterate over all flash-scoped objects using the
``{% for %}`` tag if you want to:

.. code-block:: html+django

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


.. seealso::
   :mod:`djangoflash.context_processors` module.

